# TimeTable_Generator

This project is used to generate an on-duty timetable for teachers.

## Current Progress

- Design teacher management: bug for not save teacher to database

## Database

SQLite

This project use SQLite as the database to store the data of teacher, room and session.

- Teacher Table

```
CREATE TABLE TEACHER (
    teacher_id TEXT PRIMARY KEY, -- a 6-bit unique id to indicate a teacher
    name TEXT NOT NULL, -- name of a teacher
    salary REAL NOT NULL, -- hour salary of a teacher
    available_date TEXT NOT NULL, -- the days of the month a teacher is able to be on-duty, format is ["xx/xx", "xx/xx", ...]
    start_time TEXT NOT NULL, -- the time that teacher starts working of the day, format is xx:xx
    end_time TEXT NOT NULL, -- the time that teacher ends working of the day, format is xx:xx
    working_hr REAL NOT NULL, -- the total working hours of a teacher in the month
    auto_working_token INTEGER NOT NULL, -- number of on-duty times in this month, assigned by algorithm
    assign_working_token INTEGER NOT NULL, -- number of on-duty times in this month, assigned by user
    total_working_token INTEGER GENERATED ALWAYS AS (auto_working_token + assign_working_token) STORED, -- auto_working_token + assign_working_token
    on_duty_session TEXT -- a list of session_id that the teacher is on-duty
);

```

- Room Table

```
CREATE TABLE ROOM (
    room_id TEXT PRIMARY KEY,
    room_name TEXT NOT NULL,
    working_dates TEXT NOT NULL,
    session_list TEXT
);
```

- Session Table

```
CREATE TABLE SESSION (
    session_id TEXT PRIMARY KEY,
    session_start TEXT NOT NULL,
    session_end TEXT NOT NULL,
    session_room TEXT NOT NULL,
    session_date TEXT NOT NULL,
    student_count INTEGER NOT NULL,
    on_duty_teachers TEXT,
    session_token INTEGER NOT NULL
);
```

## Feature

### teacher.py

`teacher` object indicate a real teacher working in our company, we need to assign teachers into different rooms of different sessions.

- `__init__()`

  - This method is used to create a new `teacher` object and add this object as a record into the `TEACHER` table of `timetable_generator.db`.
  - `teacher` object attribute:
    - `teacher_id`(string of int): a 6-bit unique id to indicate a teacher
    - `name`(string): name of a teacher
    - `salary`(float): hour salary of a teacher
    - `available_date`(list of string): the days of the month a teacher are able to on-duty, format is `["xx/xx", "xx/xx", ...]`
    - `start_time`(string): the time that teacher start working of the day, format is `xx:xx`
    - `end_time`(string): the time that teacher end worknig of the day, format is `xx:xx`
    - `working_hr`(float): the total working hours of a teacher on the month
    - `auto_working_token`(int): an integer to indicate the number of on-duty times in this month, but assign by algorithm
    - `assign_working_toekn`(int): an integer to indicate the number of on-duty times in this month, but assign by user
    - `total_working_token`(int): `auto_worknig_token` + `assign_working_token`
    - `on_duty_session`(list of `session_id`): a list of `session_id` that the `teacher` on-duty

- `edit_teacher_info()`
  - This method is used to edit the attributes of a `teacher` object and save the change to the `TEACHER` table of `timetable_generator.db`. After editting the attribute, it will call `clear_auto_schedule()` and `token_distribution()` to re-distribute the token.
- `delete_teacher()`
  - This method is used to delete a `teacher` object and delete the corresponding record into the `TEACHER` table of `timetable_generator.db`. After deleting the `teacher` object, it will call `clear_auto_schedule()` and `token_distribution()` to re-distribute the token.
    whole `time_table_generator.db`.
- `find_teacher()`
  - This method is used to search and get a `teacher` object record from `TEACHER` table of `timetable_generator.db`.
- `get_all_teachers()`
  - This method is used to get all the `teacher` object in `TEACHER` table of `timetable_generator.db`.

### room.py (TODO: need to be refactored ...)

- `__init__()`

  - This method is used to create a new `room` object and add this object as a record into the `ROOM` table of `timetable_generator.db`.
  - `room` object attribute:
    - `room_name`(string): the name of the room
    - `room_id`(string of int): a unique 5-bit id of the room
    - `working_dates`(list of string): the dates of the room will be used in this month, format is `["xx/xx", "xx/xx", ...]`
    - `session_list`(list of `session_id`): the list of the session of the room, format is `["xxxxxxxxxxx", "xxxxxxxxxxx", ...]`

- `edit_room_info()`
  - This method is used to edit the attributes of a room and save the change into `ROOM` table of `timetable_generator.db`. After editting the attribute, it will call `clear_auto_schedule()` and `token_distribution()` to re-distribute the token and update the whole `time_table_generator.db`.
- `delete_room()`
  - This method is used to delete a `room` object and delete the corresponding record in the `ROOM` table of `timetable_generator.db`. After deleting the `room` object, it will call `clear_auto_schedule()` and `token_distribution()` to re-distribute the token and update the whole `time_table_generator.db`.
- `find_room()`
  - This method is used to search and get a `room` object record from `ROOM` table of `timetable_generator.db`.

### session.py (TODO: need to be refactored ...)

- `__init__()`
  - This method is used to create a `session` object and add this object as a record into `SESSION` table of `timetable_generator.db`.
  - `session` object attribute:
    - `session_id`(string of int): a 11-bit unique id of the session, organized by `room_id`(5-bit) + `day`(3-bit, `000` indicate `Monday`) + `session_sequence`(3-bit)
    - `session_start`(string): the starting time of the session, format is `xx:xx`
    - `session_end`(string): the ending time of the session, format is `xx:xx`
    - `session_room`(string): the `room_name` that the session belong which `room` object
    - `session_date`(string): the date of the session, format is `xx/xx`
    - `student_count`(int): number of the student in this session
    - `on_duty_teachers`(list of `teacher_id`): a list of teachers of `teacher_id` who need to onduty in this session, format is `["xxxxxx", "xxxxxx", ...]`. If a `teacher` is assigned by `manural_distribution()`, the `teacher_id` will be appended a string `"as"` to indicate this `teacher` is assigned by user(e.g. `000001as`).
    - `session_token`(int): the number of teachers are required to on-duty in this session. Each group of up to 4 students requires 1 teacher (e.g., 1 to 4 students = 1 teacher; 5 to 8 = 2 teachers; etc.).
- `edit_session_info()`
  - This method is used to edit the information of a `session` object and save the change into `SESSION` table of `timetable_generator.db`. After editting the attribute, check the `student_count` to determine whether need to update the `session_token`. Then, it will call `clear_auto_schedule()` and `token_distribution()` to re-distribute the token and update the whole `time_table_generator.db`.
- `delete_session()`
  - This method is used to delete a `session` and delete the corresponding record in the `SESSION` table of `timetable_generator.db`. After deleting the `SESSION` object, it will call `clear_auto_schedule()` and `token_distribution()` to re-distribute the token and update the whole `time_table_generator.db`.
- `find_session()`
  - This method is used to search and get a `session` object record from `SESSION` table of `timetable_generator.db`.

### schedule.py

- `clear_auto_schedule()`

  - This method is used to clear all `teacher_id` except those end with `"as"` in every `session`'s `on_duty_teachers` list.

    When remove a `teacher_id` from the `on_duty_teachers` list, the corresponding `teacher`'s `working_hr`, `auto_working_token`, `total_working_token` and `on_duty_session` should be updated.

    Finally, these change will updated to the `timetable_generator.db`.

- `token_distribution()`

  - This method is used to distribute the token of every session.

    For each `session`, the method will get the `session_token` and `on_duty_teachers` of the `session`. If `len(on_duty_teachers)` not fulfill the `session_token`, the method will start to loop for the number of vacancy, until there are enough `teacher` for this `session`.

    In each loop, the method will use Min Heap to search the `teacher` object with the smallest `total_working_token`. Then, this `teacher`'s `teacher_id` will be appended to the `session`'s `on_duty_teacher` and this `teacher`'s `auto_working_token` increases by 1 and also update the `total_working_token`, `working_hr`, `on_duty_session`.

    Finally, these change will be updated to the `timetable_generator.db`.

- `manural_distribution()`

  - This method is used to allow user to assign a `teacher` to certain `session` manuraly.

    This method will accpet 2 args: `teacher`, `session_object_list`

    This method will call `clear_auto_schedule()` to remove all data first.

    Then, this method will loop for `len(session_object_list)`. In each loop, the method will get the `session` object in the `session_object_list`, and update `teacher`'s `working_hr`, `assign_working_token`, `total_working_token` and `on_duty_session`. Also, the `teacher`'s `teacher_id` should be appended to the `session`'s `on_duty_teachers` with the end of `"as"` to indicate that the `teacher` is assinged manurally not auto distributed.

    Then, this method will call `token_distribution` to do the auto distribution.

    Finally, these change will be updated to the `timetable_generator.db`.

- `remove_teacher()`

  - This method is used to remove a `teacher` from `session`(s).

    This method will accept two args: `teacher` and `session_object_list`.

    First, this method will loop for `len(session_object_list)`. In each loop, the method will get the `session` object in the `session_object_list`, and remove `teacher`'s `teacher_id` from the `session`'s `on_duty_teacher` list.

    Moreover, if the removed `teacher_id` is ended with `"as"`, update the `teacher`'s `assign_working_token`. Otherwise, update `teacher`'s `auto_working_token`.

    Then, update the corresponding `teacher`'s `working_hr`, `on_duty_session`, and `total_working_token`.

### database.py

This file is used to handle the database operation.

### ui_display.py

### room_management.py

### session_management.py

### teacher_management.py
