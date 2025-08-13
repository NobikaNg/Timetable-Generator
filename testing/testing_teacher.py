from src.models.teacher import Teacher

# Initialize the Teacher class
teacher = Teacher()

# Add a teacher
# teacher.add_teacher(
#     teacher_id="000001",
#     name="John Doe",
#     salary=50.0,
#     available_date=["07/31", "08/01"],
#     start_time="09:00",
#     end_time="17:00",
#     working_hr=160.0,
#     auto_working_token=5,
#     assign_working_token=3,
#     on_duty_session=["00001001001"]
# )

# teacher.delete_teacher("")

# Verify the teacher was added
result = teacher.find_teacher("000001")
print(result)