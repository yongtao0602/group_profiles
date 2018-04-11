create table group_portrait_jobs(
    id int not null auto_increment,
	job_name varchar(128),
	user_name varchar(32),
	job_status char(32),
  	params varchar,
    file varchar,
    submit_day date,
    finish_day date,
    )
character set = utf8;