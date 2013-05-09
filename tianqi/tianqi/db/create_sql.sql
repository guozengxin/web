drop table if exists cityinfo;

create table cityinfo (
	cityid int(11) not null,
	url varchar(256) not null,
	name varchar(256) not null,
	parentcityid int(11),
	primary key (cityid)
);

drop table if exists tianqiinfo;

create table tianqiinfo (
	date date not null,
	cityid int(11) not null,
	mintemperature varchar(20),
	maxtemperature varchar(20),
	windstatus varchar(100),
	weatherstatus varchar(100),
	c_temperature varchar(20),
	c_relativehumidity varchar(20),
	c_windorientation varchar(20),
	c_windpower varchar(20),
	lifetips varchar(255),
	lastupdate timestamp,
	primary key (date, cityid)
);
