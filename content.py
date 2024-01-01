from enum import Enum
from bale import (
    Message,
)


class RegisterMode(Enum):
    FIRST_NAME = "first_name"
    LAST_NAME = "last_name"
    NATIONAL_CODE = "national_code"
    GRADE = "grade"
    PHONE_NUMBER = "phone_number"
    SELECT_SCHOOL = "school"
    PICK_BIRTHDAY = "birthday"
    HAVE_LAPTOP = "have_laptop"
    PROGRAMMING_LEVEL = "programming_level"
    SOCIAL_ACTIVITY = "social_activity"
    FUTURE_FILD = "future_fild"
    WICH_TOWN = "town"


SAY_WELLCOME = """سلام رفیق!
تا همین جا هم که اومدی یعنی کارت درسته.
خب! قطعا میدونی که این ربات برای ثبت نام توی دوره »ایران آینده« طراحی شده. از اونجایی که توی این دوره فقط کلاس نهمی و دهمی های ریاضی رو ثبت نام میکنیم؛
اگه جز این بچه ها نیستی یواشکی ثبت نام کن😉
احتمالش کمه که قبول بشی ولی ناامید هم نشو. شاید تو تنها استثنای این دوره باشی.
خب دیگه خیلی حرف زدیم بریم سراغ ثبت نام."""

INPUT_NAME = "نام و نام خواندگی رو ارسال کنید:"

personality_qustion = {
    RegisterMode.FIRST_NAME: "اسمت چیه؟ (فقط اسم کوچیک)",
    RegisterMode.LAST_NAME: "فامیلیت چیه؟",
    RegisterMode.NATIONAL_CODE: "کد ملی ات چنده؟",
    RegisterMode.SELECT_SCHOOL: "توی چه مدرسه ای درس میخونی؟",
    RegisterMode.PHONE_NUMBER: "یه شماره تلفن همراه هم وارد کن. (اگه خودت موبایل نداری تفلن مامان یا بابا رو بده)",
    RegisterMode.GRADE: "کاس چندمی؟",
    RegisterMode.PICK_BIRTHDAY: "تاریخ تولدت رو وارد کن. مثلا این شکلی(1375/8/6)",
    RegisterMode.HAVE_LAPTOP: "لپ تاپ داری؟ (اگه مال مامان و بابا هم باشه بتونی ازشون قرض بگیری هم قبوله) توجه کن که لپ تاپ داشتن این امتیازی برای ثبت نام به حساب نمیاد.",
    RegisterMode.PROGRAMMING_LEVEL: "چقدر با برنامه نویسی آشنا هستی؟",
    RegisterMode.SOCIAL_ACTIVITY: "کجا فعالیت میکنی؟",
    RegisterMode.FUTURE_FILD: "چه رشتی ای هستی؟ یا در آینده چه رشته ای میخوای بری؟",
    RegisterMode.WICH_TOWN: "خونه تون کجاست؟ _(توی چه محله ای)",
}
future_fild_list = ["ریاضی", "تجربی", "انسانی", "هنرستان"]
have_laptop_list = ["دارم", "ندارم"]
list_of_schools = [
    "دستغیب 1",
    "دستغیب 2",
    "محمد رسول الله",
    "توحید",
    "اندیشه",
    "شاکرین",
]

list_of_grade = ["هفتم", "هشتم", "نهم", "دهم", "یازدهم", "دوازدهم"]

list_of_programming_level = [
    "حرفه ای",
    "کم و بیش",
    "آشنایی با کامپیوتر",
    "صرفا علاقه دارم",
]

social_activity_list = ["بسیج محله", "هیئت", "مدرسه", "فعالیت های فرهنگی خارج از مدرسه"]