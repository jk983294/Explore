create table user (
    id int(11) not null auto_increment,
    name varchar(50) character set latin1 not null,
    pswd varchar(50) character set latin1 default null,
    primary key (id)
) engine=MYISAM auto_increment=1 default charset=gbk;