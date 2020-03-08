-- 创建用户表
create table user (
	id int primary key auto_increment,
	name varchar(20),
	password varchar(40)
)

insert into user values (null, 'jack', '123'),(null,'rose','456');