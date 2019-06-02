create view student_summary as select students.id id,
 students.first_name first_name, 
 students.last_name last_name , 
 students.dormitory dormitory,
 (select cohorts.name from cohorts where  id =students.cohort_id) cohort, 
 (select pets.name from pets where  id =students.pet_id) pet,
 (select transport_types.name from  transport_types where  id =students.transport_type_id) transport,
 (select AVG(students_assignments.value) from  students_assignments  where student_id = students.id )  mean_assignment_value
 from students
 group by id;