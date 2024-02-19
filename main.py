import csv
import time

import pymongo
from bale import (
    Bot,
    CallbackQuery,
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,

    User, InputFile,
)

from content import (
    SAY_WELLCOME,
    personality_qustion,
    RegisterMode,
    list_of_schools,
    list_of_grade,
    list_of_programming_level,
    social_activity_list,
    future_fild_list,
    have_laptop_list, SAY_BYE, chanel_address, register_mode_fild_name, MENU_LIST, SAY_FINISHED, sex_list, IQQuestion,
)
from iq import remove_all_iq_question_from_user
from setting import BALE_TOKEN, BACKUP_CHANEL
from utils.menu import create_menu, edit_menu
from utils.national_code_checker import verify_national_code

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["baleBotDB"]
db = mydb["students"]

client = Bot(token=BALE_TOKEN)


@client.event
async def on_ready():
    print(client.user, "is Ready!")


def send_register_data_until_now(user: User):
    student = get_student_from_user(user)
    message = ''
    for item in student:
        if item != '_id':
            message += student[item] + '\n'
    user.send(message)


selection_button_list = {
    RegisterMode.SELECT_SCHOOL: list_of_schools,
    RegisterMode.GRADE: list_of_grade,
    RegisterMode.PROGRAMMING_LEVEL: list_of_programming_level,
    RegisterMode.FUTURE_FILD: future_fild_list,
    RegisterMode.SOCIAL_ACTIVITY: social_activity_list,
    RegisterMode.HAVE_LAPTOP: have_laptop_list,
    RegisterMode.SEX: sex_list
}


def reply_to_answer_message(user: User, mode: RegisterMode) -> str:
    student = get_student_from_user(user)  # type: ignore
    if student:
        if mode == RegisterMode.FIRST_NAME:
            first_name = student[RegisterMode.FIRST_NAME.value]
            return f"پس اسم قشنگت {first_name} هست."
        if mode == RegisterMode.LAST_NAME:
            first_name = student[RegisterMode.FIRST_NAME.value]
            last_name = student[RegisterMode.LAST_NAME.value]
            return f"{first_name} {last_name} عزیز"
        if mode == RegisterMode.NATIONAL_CODE:
            first_name = student[RegisterMode.FIRST_NAME.value]
            last_name = student[RegisterMode.LAST_NAME.value]
            national_code = student[RegisterMode.NATIONAL_CODE.value]
            return f"{first_name} {last_name} با کد ملی {national_code}"
        if mode == RegisterMode.SELECT_SCHOOL:
            school = student[RegisterMode.SELECT_SCHOOL.value]
            return f"دمت گرم پسر! واقعا توی مدرسه {school} درس میخونی؟"
        if mode == RegisterMode.PHONE_NUMBER:
            phone_number = student[RegisterMode.PHONE_NUMBER.value]
            return f"خب شماره ای که وارد کردی همینه؟\n{phone_number}"
        if mode == RegisterMode.GRADE:
            grade = student[RegisterMode.GRADE.value]
            if grade not in ["نهم", "دهم"]:
                return f"نگاه کن ما برنامه مون اینه که فقط واسه نهمی ها و دهمی های ریاضی دوره رو برگزار کنیم. ولی حالا تو هم ثبت نام کن. شاید دیدی ...\n پس کلاس {grade} هستی؟"
            return f"پس کلاس {grade} هستی!"
        if mode == RegisterMode.PROGRAMMING_LEVEL:
            programming_level = student[RegisterMode.PROGRAMMING_LEVEL.value]
            return f"در سطح {programming_level} هستی؟"
        if mode == RegisterMode.HAVE_LAPTOP:
            have_laptop = student[RegisterMode.HAVE_LAPTOP.value]
            return f"مطمئن هستی؟ گفتی {have_laptop}"
        if mode == RegisterMode.WICH_TOWN:
            town = student[RegisterMode.WICH_TOWN.value]
            return f"پس بچه‌ی {town} هستی؟"
        if mode == RegisterMode.SOCIAL_ACTIVITY:
            social_activity = student[RegisterMode.SOCIAL_ACTIVITY.value]
            return f"پس توی {social_activity} فعالیت میکنی"
        if mode == RegisterMode.FUTURE_FILD:
            future_fild = student[RegisterMode.FUTURE_FILD.value]
            return f"{future_fild} رو عشقه"
        if mode == RegisterMode.PICK_BIRTHDAY:
            birthday = student[RegisterMode.PICK_BIRTHDAY.value]
            return f"تاریخ تولدت همینه؟ {birthday}"

    return "به خطا خوریدم!"


async def say_hello(message: Message, component=None):
    await message.chat.send(SAY_WELLCOME, components=component)


def answer_checker(message: Message) -> bool:
    if message.text:
        return message.text not in MENU_LIST and message.text not in ['/start']
    return False


def get_student_from_user(user: User):
    student = db.find_one({"_id": str(user.user_id)})
    return student


def update_student(user: User, data: dict):
    db.update_one({"_id": f"{user.user_id}"}, {"$set": data})


async def select_step(user: User):
    student = get_student_from_user(user)
    if student:
        if RegisterMode.FIRST_NAME.value not in student:
            await register_first_name(user)
        elif RegisterMode.LAST_NAME.value not in student:
            await register_last_name(user)
        elif RegisterMode.SEX.value not in student:
            await select_sex(user)
        elif RegisterMode.NATIONAL_CODE.value not in student:
            await register_national_cod(user)
        elif RegisterMode.SELECT_SCHOOL.value not in student:
            await select_school(user)
        elif RegisterMode.PHONE_NUMBER.value not in student:
            await register_mobile_phone(user)
        elif RegisterMode.GRADE.value not in student:
            await select_grade(user)
        elif RegisterMode.PICK_BIRTHDAY.value not in student:
            await register_birthday(user)
        elif RegisterMode.PROGRAMMING_LEVEL.value not in student:
            await select_programming_level(user)
        elif RegisterMode.FUTURE_FILD.value not in student:
            await select_future_fild(user)
        elif RegisterMode.HAVE_LAPTOP.value not in student:
            await select_have_laptop(user)
        elif RegisterMode.SOCIAL_ACTIVITY.value not in student:
            await select_social_activity(user)
        elif RegisterMode.WICH_TOWN.value not in student:
            await register_town(user)
        else:
            for iq in IQQuestion:
                if f'IQ-{iq.value}' not in student:
                    from iq import iq_question_callback
                    if iq in [IQQuestion.Q2, IQQuestion.Q3, IQQuestion.Q4]:
                        update_student(user, {'finished': False})
                        res = await iq_question_callback[iq](user, client)
                        update_student(user, res)
                        await select_step(user)
                    else:
                        await iq_question_callback[iq](user)
                    return
                elif f'IQ-{iq.value}' == 'IQ-q10':
                    update_student(user, {'finished': True})
            if student['finished']:
                backup_message_id = student['backup_message_id']
                # if BACKUP_CHANEL:
                # await client.edit_message(BACKUP_CHANEL, backup_message_id, text=student_info(student))
                await user.send(SAY_FINISHED, components=create_menu())
            else:
                if BACKUP_CHANEL:
                    message = await client.send_message(BACKUP_CHANEL, text=student_info(student))
                    update_student(user, {'backup_message_id': message.message_id, 'finished': True})
                await user.send(SAY_BYE, components=create_menu())


async def select_button(user: User, mode: RegisterMode):
    markup_select = InlineKeyboardMarkup()
    for i in range(len(selection_button_list[mode])):
        if '/' in selection_button_list[mode][i]:
            data = selection_button_list[mode][i]
        else:
            data = i
        markup_select.add(
            InlineKeyboardButton(
                text=selection_button_list[mode][i],
                callback_data=f"{mode.value}:{data}",
            ),
            row=i + 1,
        )
    await user.send(personality_qustion[mode], components=markup_select)


async def save_button_selection(user: User, data: str, iq_question_mode=False):
    callback_data = data.split(":")
    str_mode = callback_data[0]
    index_of_button = int(callback_data[1])
    if iq_question_mode:
        update_student(user, {str_mode: index_of_button})  # type: ignore
    else:
        update_student(user, {str_mode: selection_button_list[RegisterMode(str_mode)][index_of_button]})  # type: ignore
        await reply_to_answer(user, RegisterMode(str_mode))


def student_info(student: dict):
    message = ''
    for fild in student:
        if fild not in ['_id', 'finished', 'backup_message_id']:
            if fild in [r.value for r in RegisterMode]:
                mode = RegisterMode(fild)
                title = register_mode_fild_name[mode]
            else:
                continue
            message += f'{title}: {student[fild]}\n'
    return message


async def register_first_name(user: User):
    await register_personality(user, RegisterMode.FIRST_NAME)


async def register_last_name(user: User):
    await register_personality(user, RegisterMode.LAST_NAME)


async def register_national_cod(user: User):
    await register_personality(user, RegisterMode.NATIONAL_CODE, verify_national_code)


async def register_mobile_phone(user: User):
    await register_personality(user, RegisterMode.PHONE_NUMBER)


async def register_town(user: User):
    await register_personality(user, RegisterMode.WICH_TOWN)


async def register_birthday(user: User):
    await register_personality(user, RegisterMode.PICK_BIRTHDAY)


async def select_school(user: User):
    await select_button(user, RegisterMode.SELECT_SCHOOL)


async def write_school(user: User):
    await register_personality(user, RegisterMode.SELECT_SCHOOL)


async def select_grade(user: User):
    await select_button(user, RegisterMode.GRADE)


async def select_sex(user: User):
    await select_button(user, RegisterMode.SEX)


async def select_programming_level(user: User):
    await select_button(user, RegisterMode.PROGRAMMING_LEVEL)


async def select_future_fild(user: User):
    await select_button(user, RegisterMode.FUTURE_FILD)


async def select_have_laptop(user: User):
    await select_button(user, RegisterMode.HAVE_LAPTOP)


async def select_social_activity(user: User):
    await select_button(user, RegisterMode.SOCIAL_ACTIVITY)


function_map = {
    RegisterMode.FIRST_NAME: register_first_name,
    RegisterMode.LAST_NAME: register_last_name,
    RegisterMode.NATIONAL_CODE: register_national_cod,
    RegisterMode.GRADE: select_grade,
    RegisterMode.PHONE_NUMBER: register_mobile_phone,
    RegisterMode.SELECT_SCHOOL: select_school,
    RegisterMode.PICK_BIRTHDAY: register_birthday,
    RegisterMode.HAVE_LAPTOP: select_have_laptop,
    RegisterMode.PROGRAMMING_LEVEL: select_programming_level,
    RegisterMode.SOCIAL_ACTIVITY: select_social_activity,
    RegisterMode.FUTURE_FILD: select_future_fild,
    RegisterMode.WICH_TOWN: register_town
}


async def reply_to_answer(
        user: User,
        mode: RegisterMode,
        verify_needed: bool = False
):
    if not verify_needed:
        await select_step(user)
        return
    else:
        message_reply = reply_to_answer_message(user, mode)
        reply_markup_verify_name = InlineKeyboardMarkup()
        reply_markup_verify_name.add(
            InlineKeyboardButton(text="آره", callback_data=f"{mode.value}:accept")
        )
        reply_markup_verify_name.add(
            InlineKeyboardButton(text="ویرایش", callback_data=f"{mode.value}:reject")
        )
    await user.send(
        message_reply,
        components=reply_markup_verify_name,
    )


async def register_personality(user: User, mode: RegisterMode, check_func=None):
    await user.send(personality_qustion[mode])
    student_answer = await client.wait_for("message", check=answer_checker)
    if student_answer:
        if check_func and not check_func(student_answer.content):
            await student_answer.reply('مقدار وارد شده صحیح نمیباشد.')
            return register_personality(user, mode, check_func)
        elif student_answer.from_user:
            update_student(student_answer.from_user, {mode.value: student_answer.content})
        else:
            print("error in student_answer")

    await reply_to_answer(student_answer.from_user, mode)


def backup():
    dv_cursor = db.find()
    list_of_student = []
    for i in dv_cursor:
        list_of_student.append(i)
    keys = list_of_student[0].keys()
    with open('backup.csv', 'w+') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(list_of_student)
    with open('backup.csv', 'rb') as upload_file:
        file = InputFile(upload_file.read())
        return file


@client.event
async def on_message(message: Message):
    student = get_student_from_user(message.from_user)
    if message.content == '/backup':
        file = backup()
        await client.send_document(BACKUP_CHANEL, file, caption=f'{time.ctime(time.time())}')
        await message.reply('done')

    elif message.content in ['/start', '/شروع (ادامه)']:
        if not student:
            menu = create_menu()
            await say_hello(message, menu)
            db.insert_one({"_id": f"{message.from_user.user_id}", 'finished': False})
        await select_step(message.from_user)  # type: ignore
    elif message.content == '/ویرایش' or message.content == '/edit':
        menu = edit_menu()
        await message.reply("کدام قسمت را میخواهید تغییر دهید؟", components=menu)
    elif message.content == '/کانال':
        await message.reply(text=chanel_address)
    elif message.content == '/مشاهده_اطلاعات':
        student_info_message = student_info(student)
        await message.reply(text=student_info_message)
    elif message.content == '/edit_iq_test':
        remove_all_iq_question_from_user(message.from_user, db)
        await select_step(message.from_user)


@client.event
async def on_callback(callback: CallbackQuery):
    message = callback.message
    user = callback.user
    if "accept" in callback.data:
        await select_step(user)
    elif 'reject' in callback.data:
        mode = callback.data.split(':')[0]
        await function_map[RegisterMode(mode)](message.from_user)
    elif 'edit' in callback.data:
        value_mode = callback.data.split(':')[0]
        mode = RegisterMode(value_mode)
        await function_map[mode](user)
    elif "/مدارس‌ دیگر" in callback.data:
        await write_school(user)
    elif (

            RegisterMode.SELECT_SCHOOL.value in callback.data
            or RegisterMode.GRADE.value in callback.data
            or RegisterMode.PROGRAMMING_LEVEL.value in callback.data
            or RegisterMode.HAVE_LAPTOP.value in callback.data
            or RegisterMode.FUTURE_FILD.value in callback.data
            or RegisterMode.SOCIAL_ACTIVITY.value in callback.data
            or RegisterMode.SEX.value in callback.data
    ):
        await save_button_selection(user, callback.data)
    elif "IQ-" in callback.data:
        await save_button_selection(user, callback.data, iq_question_mode=True)
        await select_step(user)


while True:
    try:
        client.run()
    except Exception as ex:
        print(ex)
