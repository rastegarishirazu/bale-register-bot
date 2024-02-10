from bale import User, InlineKeyboardMarkup, InlineKeyboardButton

from content import IQQuestion, iq_question_content

iq_question_list = [iq.name for iq in IQQuestion]


async def question_option(user: User, question: IQQuestion):
    markup_select = InlineKeyboardMarkup()
    for i in range(1, 5):
        markup_select.add(InlineKeyboardButton(
            text=f'گزینه {i}',
            callback_data=f"IQ-{question.value}:{i}"
        ), row=i + 1
        )
    await user.send(iq_question_content[question], components=markup_select)


async def descriptive_question(user: User, client, question: IQQuestion, check_func=None):
    await user.send(iq_question_content[question])
    student_answer = await client.wait_for(event_name="message")
    if check_func and not check_func(student_answer.content):
        await student_answer.reply('مقدار وارد شده صحیح نمیباشد.')
        return descriptive_question(user,client, question, check_func)
    elif student_answer.from_user:
        return {f'IQ-{question.value}': student_answer.content}


def check_graph_question(text):
    try:
        value = int(text)
        return True
    except:
        return False


async def iq_test_q2(user: User, client):
    return await descriptive_question(user, client, IQQuestion.Q2, check_graph_question)


async def iq_test_q3(user: User, client):
    return await descriptive_question(user, client, IQQuestion.Q3, check_graph_question)


async def iq_test_q4(user: User, client):
    return await descriptive_question(user, client, IQQuestion.Q4, check_graph_question)


async def iq_test_q5(user: User):
    await question_option(user, IQQuestion.Q5)


async def iq_test_q6(user: User):
    await question_option(user, IQQuestion.Q6)


async def iq_test_q7(user: User):
    await question_option(user, IQQuestion.Q7)


async def iq_test_q8(user: User):
    await question_option(user, IQQuestion.Q8)


async def iq_test_q9(user: User):
    await question_option(user, IQQuestion.Q9)


async def iq_test_q10(user: User):
    await question_option(user, IQQuestion.Q10)


iq_question_callback = {
    IQQuestion.Q2: iq_test_q2,
    IQQuestion.Q3: iq_test_q3,
    IQQuestion.Q4: iq_test_q4,
    IQQuestion.Q5: iq_test_q5,
    IQQuestion.Q6: iq_test_q6,
    IQQuestion.Q7: iq_test_q7,
    IQQuestion.Q8: iq_test_q8,
    IQQuestion.Q9: iq_test_q9,
    IQQuestion.Q10: iq_test_q10,

}
