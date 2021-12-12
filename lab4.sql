drop database if exists lab4;
create database if not exists lab4;
use lab4;



/*
    创建客户表
*/
create table `customer`(
    `cid` int(32) not null AUTO_INCREMENT,
    `phone` varchar(64) not null,
    `address` varchar(128) not null,
    `email` varchar(64) not null,
    `card` char(64) not null,
    `first_name` varchar(64) not null,
    `last_name` varchar(64) not null,
    `gender` varchar(10),
    primary key(`cid`)
);

insert  into customer(cid ,last_name, first_name, address, phone, email, card, gender) value
(62,'Murray','Annabelle','59 W. Central Ave','404-998-3928','belle@comcast.net','443355463212', 'male'),
(59,'Franco','Gina','1012 Peachtree St','404-887-2342','gf59@gmail.com','443398764532', 'male'),
(13,'Quinn','Sally','54 Oak Ave','404-987-3427','quinn45@gmail.com','443398765439', 'female'),
(29,'Lopato','Maria','5490 West 5th','404-234-8876','mrl@hotmail.com','443352635423', 'female'),
(30,'Zern','Joan','58 W. Central Ave','404-675-0091','zern@comcast.net','443357643254', 'male'),
(63,'Smith','Patricia','1700 E. Lincoln Ave','404-765-3342','patti1@gmail.com','443398762534', 'male'),
(91,'Pao','Jill','89 Orchard','404-887-9238','pao@comcast.net','443367256543', 'female'),
(17,'Berry','Anna','9 Pleasant Way','404-887-4673','aberry@hotmail.com','443376562837', 'male');




/*
    创建设计师表
    price           标记该设计师设计的包应付每日租金
*/
create table `designer`(
    `did` int(32) not null AUTO_INCREMENT,
    `name` varchar(64) not null,
    `price` double(32,2) not null,
    primary key(`did`)
);

INSERT INTO designer(name, price) value
('Louis Vuitton',8.75),
('Prada',9.50),
('Coach',9.00),
('Burberry',10.00);




/*
    创建奢侈包的表
    already_rented  标记该包是否已经租赁出去且未归还
    did             标记该包的设计师 id
*/
create table `bag`(
    `bid` int(32) not null AUTO_INCREMENT,
    `type` varchar(32) not null,
    `color` varchar(32) not null,
    `did` int(32) not null,
    `already_rented` tinyint(1) not null default 0,
    primary key(`bid`),
    foreign key(`did`) references `designer`(`did`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO bag(bid, type,color, did) value
(101,'Claudia','White',1),
(102,'Cabas Piano','Multi',1),
(103,'Monogram Pochette','Multi',1),
(104,'Satchel','Camel',3),
(105,'Hippie Flap','Green',3),
(106,'Bleeker Bucket','Blue',3),
(107,'Messenger','Black', 2),
(108,'Fairy','Multi', 2),
(109,'Glove Soft Pebble','Mauve', 2),
(110,'Haymarket Woven Warrier','Gold',4),
(111,'Knight','Plaid',4);



/*
    创建租赁单据的表
    rid                 标记单个租赁交易
    cid                 标记用户 id
    bid                 标记被租赁的包的 id
    optional_insurance  标记该租赁交易是否购买了保险
*/
create table `rentals`(
    `rid` int(32) not null AUTO_INCREMENT,
    `cid` int(32) not null,
    `bid` int(32) not null,
    `date_rented` date default null,
    `date_returned` date default null,
    `optional_insurance` boolean default false,
    primary key(`rid`),
    foreign key(`cid`) references `customer`(`cid`),
    foreign key(`bid`) references `bag`(`bid`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO rentals (cid, bid, date_rented, date_returned, optional_insurance) value
(62,101,'2011/4/12','2011/4/30',TRUE),
(62,107,'2011/1/19','2011/2/1',TRUE),
(59,102,'2011/2/11','2011/2/19',TRUE),
(59,104,'2011/3/9','2011/3/11',TRUE),
(59,105,'2011/5/21','2011/5/25',TRUE),
(13,110,'2011/3/16','2011/3/17',FALSE),
(29,106,'2011/5/18','2011/5/25',FALSE),
(30,108,'2011/1/1','2011/2/1',TRUE),
(30,101,'2011/6/2','2011/6/8',TRUE),
(30,103,'2011/5/6','2011/5/9',TRUE),
(63,109,'2011/6/2','2011/6/30',FALSE),
(91,111,'2011/2/19','2011/3/1',TRUE),
(91,111,'2011/3/30','2011/4/2',TRUE),
(17,101,'2011/3/5','2011/3/9',FALSE),
(17,103,'2011/4/1','2011/4/21',FALSE),
(17,106,'2011/5/5','2011/5/9',FALSE);



/*
    存储过程
    展示所有表名
*/
delimiter //
create procedure show_all_tables()
begin
    show tables;
end //
delimiter;



/*
    存储过程
    展示指定表的表头字段
    传入参数为表名
*/
delimiter //
create procedure show_columns_from_table(in tableName varchar(30))
begin
    set @sql = concat('show columns from ', tableName);
    prepare stmt from @sql;
    execute stmt;
    deallocate prepare stmt;
end; //
delimiter;

-- call show_columns_from_table('bag')



/*
    存储过程
    展示指定的表内容
    传入参数为表名
*/
delimiter //
create procedure show_table(in tableName varchar(30))
begin
    set @sql = concat('select * from ', tableName);
    prepare stmt from @sql;
    execute stmt;
    deallocate prepare stmt;
end; //
delimiter;



/*
    存储过程
    计算指定表中有多少行数据
    传入参数为表名
*/
delimiter //
create procedure get_cnt_table(in tableName varchar(30))
begin
    set @sql = concat('select count(*) from ', tableName);
    prepare stmt from @sql;
    execute stmt;
    deallocate prepare stmt;
end; //
delimiter;



/*
    存储过程
    获取所有客户 id
 */
delimiter //
create procedure get_customers_id()
begin
    select cid from customer;
end; //
delimiter;




/*  
    存储过程
    获取所有设计师的名字
 */
delimiter //
create procedure get_designers_name()
begin
    select name from designer;
end; //
delimiter;



/*
    存储过程
    创建显示每个设计师设计了多少包
    传入参数  designer  为该设计师名字
*/
delimiter //
create procedure bag_by_designer(in designer varchar(30))
begin
    select 
        type as 'Name', 
        color as 'Color', 
        d.name as 'Manufacturer' 
    from bag as b
    left join designer as d
    on b.did = d.did
    where d.name = designer;
end //
delimiter;

-- call bag_by_designer('Coach');



/*
    存储过程
    创建 按照所有交易总租赁奢侈包总天数排序 显示客户
*/
delimiter //
create procedure best_customers()
begin 
    select 
        last_name as 'Last Name',
        first_name as 'First Name',
        address as 'Address',
        phone as 'Telephone',
        ifnull(sum(datediff( date_returned, date_rented)), 0) 
            as 'Total Length of Rentals' 
    from customer as c 
    left join rentals as r 
    on c.cid = r.cid 
    group by c.cid 
    order by `Total Length of Rentals` desc;
end //
delimiter;

-- call best_customers();



/*
    存储过程
    按照用户 id 计算 用户每个租赁交易应支付 账单金额 从大到小排序
    传入参数为用户 id
*/
delimiter //
create procedure report_customer_amount(in customer_id int(32))
begin
    select 
        c.last_name as 'Last Name',
        c.first_name as 'First Name',
        d.name as 'Manufacturer',
        b.type as 'Name',
        datediff( r.date_returned, r.date_rented) as 'totalDays',
        (d.price + r.optional_insurance) 
            * datediff( r.date_returned, r.date_rented) as 'Cost'
    from rentals as r 
    left join customer as c 
    on r.cid = c.cid 
    left join bag as b 
    on r.bid = b.bid 
    left join designer as d 
    on d.did = b.did 
    where r.cid = customer_id
    order by Cost desc;
    
end //
delimiter;

-- call report_customer_amount(17);



/*
    存储过程
    按照用户 id 计算 用户每个租赁交易应支付 账单金额 从小到大排序
    传入参数为用户 id
*/
delimiter //
create procedure report_customer_amount2(in customer_id int(32))
begin
    select 
        c.last_name as 'Last Name',
        c.first_name as 'First Name',
        d.name as 'Manufacturer',
        b.type as 'Name',
        datediff( r.date_returned, r.date_rented) as 'totalDays',
        (d.price + r.optional_insurance) 
            * datediff( r.date_returned, r.date_rented) as 'Cost'
    from rentals as r 
    left join customer as c 
    on r.cid = c.cid 
    left join bag as b 
    on r.bid = b.bid 
    left join designer as d 
    on d.did = b.did 
    where r.cid = customer_id
    order by Cost desc;
    
end //
delimiter;

/*
    存储过程
    按照用户 id 计算 用户所有租赁交易应支付 账单金额 
    传入参数为用户 id
*/
delimiter //
create procedure report_customer_totalCost(in customer_id int(32))
begin
    select 
        c.last_name as 'Last Name',
        c.first_name as 'First Name',
        sum((d.price + r.optional_insurance) 
            * datediff( r.date_returned, r.date_rented)) as totalCost
    from rentals as r 
    left join customer as c 
    on r.cid = c.cid 
    left join bag as b 
    on r.bid = b.bid 
    left join designer as d 
    on d.did = b.did 
    where r.cid = customer_id;
end //
delimiter;

-- call report_customer_totalCost(17);



/*
    存储过程
    获取所有交易的租赁总额
*/
delimiter //
create procedure get_total_sales()
begin
    select 
        sum((d.price + r.optional_insurance) 
            * datediff( r.date_returned, r.date_rented)) as total_sales
    from rentals as r 
    left join customer as c 
    on r.cid = c.cid 
    left join bag as b 
    on r.bid = b.bid 
    left join designer as d 
    on d.did = b.did;
end //
delimiter;



/*
    存储过程
    创建租赁交易记录
    传入参数为用户 id， 奢侈品 id， 是否支付保险， 租赁天数
*/
delimiter //
create  procedure add_rentals(customerId int(32), bagId int(32), optionalInsurance tinyint(1), daysOfRent int(10))
begin
    insert into rentals(cid, bid, date_rented, date_returned, optional_insurance) 
    values (customerId, bagId, curdate(), curdate() + daysOfRent, optionalInsurance);
    update bag set already_rented = true where bid = bagId;
end //
delimiter;

-- call add_rentals(13, 101, 1, 8);



/*
    存储过程
    新建一个奢侈品背包
    传入参数为  包的类型， 包的颜色， 包的设计者
*/
delimiter //
create procedure add_bag(bagType varchar(30), bagColor varchar(10), bagDesigner varchar(30))
begin
    insert into bag( type, color, did) 
    values ( bagType, bagColor, (select did 
                                from designer
                                where name = bagDesigner));
end //
delimiter;



/*
    存储过程
    新建一个设计师
    传入参数为  设计师的名字， 设计师每个包的价格
*/
delimiter //
create procedure add_designer(dname varchar(30), price double(32,2))
begin
    
    insert into designer( name, price) 
    values (dname, price);
end //
delimiter;



/*
    存储过程
    新建一个用户
    传入参数为  first_name, last_name, 地址， 电话，邮箱，信用卡，性别
*/
delimiter //
create procedure add_customer(lname varchar(32), 
    fname varchar(32), addr varchar(128), pnum varchar(32),
    email varchar(64), cnum varchar(32), gender varchar(10))
begin
    insert into customer( last_name, first_name, address, phone, email, card, gender) 
    values (lname, fname, addr, pnum, email, cnum, gender);
end //
delimiter;



/*
    触发器
    创建会话变量 totalDays，bill
    totalDays   记录总的租赁天数
    bill        记录租赁期间应付账单金额
    update      语句更新包的租赁状态
    退回包包后可以通过执行 select 语句获取会话变量的值
*/
delimiter //
create trigger returnBag after update on rentals for each row 
begin 
    declare pricePerday double(10,2);
    set @totalDays = 0;
    set @bill = 0.00;
    if new.date_returned then 
        select 
            price into pricePerday 
            from bag as b, designer d
            where b.bid = new.bid
            and b.did = d.did;
        select 
            datediff(new.date_returned, new.date_rented) into @totalDays;
        select 
            (pricePerday + new.optional_insurance) * @totalDays into @bill;
    end if;
    update bag set already_rented = false where bid = new.bid;
end //
delimiter;

-- update rentals set date_returned = current_date where rid=18;
-- select @totalDays, @bill;
