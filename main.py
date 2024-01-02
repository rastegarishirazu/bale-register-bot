from bale import (
    Bot,
    CallbackQuery,
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    MenuKeyboardMarkup,
    MenuKeyboardButton,
    User,
)
import pymongo
from content import (
    SAY_WELLCOME,
    personality_qustion,
    RegisterMode,
    list_of_schools,
    list_of_grade,
    list_of_programming_level,
    social_activity_list,
    future_fild_list,
    have_laptop_list,
)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["baleBotDB"]
db = mydb["students"]
BOT_TOKEN = "6782619800:AAES1QsUThVE0-AdSEIVDmK_0RmMzpTV-tI"
BALE_TOKEN = "1811549661:kjsfBDLPPg2o84QZl9gvvBzlki8uFc7i787sGorS"

client = Bot(token=BALE_TOKEN)


@client.event
async def on_ready():
    print(client.user, "is Ready!")


selection_bottom_list = {
    RegisterMode.SELECT_SCHOOL: list_of_schools,
    RegisterMode.GRADE: list_of_grade,
    RegisterMode.PROGRAMMING_LEVEL: list_of_programming_level,
    RegisterMode.FUTURE_FILD: future_fild_list,
    RegisterMode.SOCIAL_ACTIVITY: social_activity_list,
    RegisterMode.HAVE_LAPTOP: have_laptop_list,
}


def reply_to_asnwer_message(user: User, mode: RegisterMode) -> str:
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


async def say_hello(message: Message):
    await message.chat.send(SAY_WELLCOME)


def answer_checker(message: Message) -> bool:
    if message.text:
        return "/start" not in message.text
    return False


def get_student_from_user(user: User):
    student = db.find_one({"_id": str(user.user_id)})
    return student


def updata_student(user: User, data: dict):
    db.update_one({"_id": f"{user.user_id}"}, {"$set": data})


async def select_step(user: User, message: Message):
    student = get_student_from_user(user)
    if student:
        if RegisterMode.FIRST_NAME.value not in student:
            await register_first_name(message)
        elif RegisterMode.LAST_NAME.value not in student:
            await register_last_name(message)
        elif RegisterMode.NATIONAL_CODE.value not in student:
            await register_national_cod(message)
        elif RegisterMode.SELECT_SCHOOL.value not in student:
            await select_school(message)
        elif RegisterMode.PHONE_NUMBER.value not in student:
            await register_mobile_phone(message)
        elif RegisterMode.GRADE.value not in student:
            await select_grade(message)
        elif RegisterMode.PICK_BIRTHDAY.value not in student:
            await register_birthday(message)
        elif RegisterMode.PROGRAMMING_LEVEL.value not in student:
            await select_programming_level(message)
        elif RegisterMode.FUTURE_FILD.value not in student:
            await select_future_fild(message)
        elif RegisterMode.HAVE_LAPTOP.value not in student:
            await select_have_laptop(message)
        elif RegisterMode.SOCIAL_ACTIVITY.value not in student:
            await select_social_activity(message)
        elif RegisterMode.WICH_TOWN.value not in student:
            await register_town(message)
        else:
            await user.send("finish")


async def select_buttom(message: Message, mode: RegisterMode):
    markup_select_school = InlineKeyboardMarkup()
    for i in range(len(selection_bottom_list[mode])):
        markup_select_school.add(
            InlineKeyboardButton(
                text=selection_bottom_list[mode][i],
                callback_data=f"{mode.value}:{i}",
            ),
            row=i // 2 + 1,
        )
    await message.chat.send(personality_qustion[mode], components=markup_select_school)


async def save_buttom_selection(user: User, data: str):
    callback_data = data.split(":")
    str_mode = callback_data[0]
    index_of_buttom = int(callback_data[1])
    updata_student(user, {str_mode: selection_bottom_list[RegisterMode(str_mode)][index_of_buttom]})  # type: ignore
    await reply_to_answer(user, RegisterMode(str_mode))


async def register_first_name(message: Message):
    await register_personality(message, RegisterMode.FIRST_NAME)


async def register_last_name(message: Message):
    await register_personality(message, RegisterMode.LAST_NAME)


async def register_national_cod(message: Message):
    await register_personality(message, RegisterMode.NATIONAL_CODE)


async def register_mobile_phone(message):
    await register_personality(message, RegisterMode.PHONE_NUMBER)


async def register_town(message):
    await register_personality(message, RegisterMode.WICH_TOWN)


async def register_birthday(message):
    await register_personality(message, RegisterMode.PICK_BIRTHDAY)


async def select_school(message):
    await select_buttom(message, RegisterMode.SELECT_SCHOOL)


async def select_grade(message):
    await select_buttom(message, RegisterMode.GRADE)


async def select_programming_level(message):
    await select_buttom(message, RegisterMode.PROGRAMMING_LEVEL)


async def select_future_fild(message):
    await select_buttom(message, RegisterMode.FUTURE_FILD)


async def select_have_laptop(message):
    await select_buttom(message, RegisterMode.HAVE_LAPTOP)


async def select_social_activity(message):
    await select_buttom(message, RegisterMode.SOCIAL_ACTIVITY)


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
):
    reply_markup_verify_name = InlineKeyboardMarkup()
    reply_markup_verify_name.add(
        InlineKeyboardButton(text="آره", callback_data=f"{mode.value}:accept")
    )
    reply_markup_verify_name.add(
        InlineKeyboardButton(text="ویرایش", callback_data=f"{mode.value}:reject")
    )
    message_reply = reply_to_asnwer_message(user, mode)

    await user.send(
        message_reply,
        components=reply_markup_verify_name,
    )


async def register_personality(message: Message, mode: RegisterMode):
    await message.chat.send(personality_qustion[mode])
    student_answer = await client.wait_for("message", check=answer_checker)
    if student_answer.from_user:
        updata_student(student_answer.from_user, {mode.value: student_answer.content})
    else:
        print("error in student_answer")
    await reply_to_answer(student_answer.from_user, mode)


@client.event
async def on_message(message: Message):
    if message.content == "/start":
        await say_hello(message)
        student = get_student_from_user(message.from_user)
        if not student:
            db.insert_one({"_id": f"{message.from_user.user_id}"})
        await select_step(message.from_user, message)  # type: ignore
        reply_markup = InlineKeyboardMarkup()
        reply_markup.add(
            InlineKeyboardButton(
                text="سلام علیکم", callback_data="python-bale-bot:help"
            )
        )


@client.event
async def on_callback(callback: CallbackQuery):
    message = callback.message
    user = callback.user
    if "accept" in callback.data:
        await select_step(user, message)
    if 'reject' in callback.data:
        mode = callback.data.split(':')[0]
        await function_map[RegisterMode(mode)]
        # if callback.data == f"{RegisterMode.FIRST_NAME.value}:reject":
        #     await function_map[RegisterMode]
        # elif callback.data == f"{RegisterMode.LAST_NAME.value}:reject":
        #     await register_last_name(message)
        # elif callback.data == f"{RegisterMode.NATIONAL_CODE.value}:reject":
        #     await register_national_cod(message)
    elif (
            RegisterMode.SELECT_SCHOOL.value in callback.data
            or RegisterMode.GRADE.value in callback.data
            or RegisterMode.PROGRAMMING_LEVEL.value in callback.data
            or RegisterMode.HAVE_LAPTOP.value in callback.data
            or RegisterMode.FUTURE_FILD.value in callback.data
            or RegisterMode.SOCIAL_ACTIVITY.value in callback.data
    ):
        await save_buttom_selection(user, callback.data)


client.run()
