create or replace procedure prc_b2b_faild_orders(days Number) is
  days_ago Number(6);
begin
  days_ago := 1;
  if (days is not null) then
    days_ago := days;
  end if;

  delete from besdev.tmp_corp_failed;
  commit;
  for i in (select t.*, to_number(substr(t.order_id, 1, 2)) as indexx
              from besorder.om_order_unclosed t
             where t.bizspecid in ('ChgCorpAcctCreditLimitOrderSpec',
                                   'CustomerOrderSpec_Corp',
                                   'TransferOwnerOrderSpec_Corp',
                                   'CorpAccountOrderSpec',
                                   'ChangeCorpCustInfoOrderSpec',
                                   'CreateCorpSubscriberOrderSpec',
                                   'ChangeCorOfferingBizSpec',
                                   'ChgCorpAcctInfoOrderSpec',
                                   'CreateCorpSubscriberOrderSpec',
                                   'ManageCorGrpMemOrderSpec',
                                   'CorpActivationOrderSpec',
                                   'GrpResSalesOrderSpec')
               and t.create_time > sysdate - days_ago) loop
    if (length(i.order_id) < 18 or (i.indexx >= 0 and i.indexx <= 19)) then
      insert into besdev.tmp_corp_failed
        select distinct b.order_id,
                        i.status,
                        b.exception_desc,
                        b.exception_trace1,
                        b.business_code,
                        b.service_number,
                        i.party_role_id,
                        'N',
                        '',
                        i.create_time,
                        b.exception_time,
                        b.processinstanceid,
                        b.retry_times,
                        row_number() over(partition by b.order_id order by b.exception_time desc) exception_num
          from besorder.om_exception b
         where i.order_id = b.order_id
           and i.be_id = b.be_id;
    elsif i.indexx >= 20 and i.indexx <= 39 then
      insert into besdev.tmp_corp_failed
        select distinct b.order_id,
                        i.status,
                        b.exception_desc,
                        b.exception_trace1,
                        b.business_code,
                        b.service_number,
                        i.party_role_id,
                        'N',
                        '',
                        i.create_time,
                        b.exception_time,
                        b.processinstanceid,
                        b.retry_times,
                        row_number() over(partition by b.order_id order by b.exception_time desc) exception_num
          from besorder.om_exception@to_bescust2 b
         where i.order_id = b.order_id
           and i.be_id = b.be_id;
    elsif i.indexx >= 40 and i.indexx <= 59 then
      insert into besdev.tmp_corp_failed
        select distinct b.order_id,
                        i.status,
                        b.exception_desc,
                        b.exception_trace1,
                        b.business_code,
                        b.service_number,
                        i.party_role_id,
                        'N',
                        '',
                        i.create_time,
                        b.exception_time,
                        b.processinstanceid,
                        b.retry_times,
                        row_number() over(partition by b.order_id order by b.exception_time desc) exception_num
          from besorder.om_exception@to_bescust3 b
         where i.order_id = b.order_id
           and i.be_id = b.be_id;
    elsif i.indexx >= 60 and i.indexx <= 79 then
      insert into besdev.tmp_corp_failed
        select distinct b.order_id,
                        i.status,
                        b.exception_desc,
                        b.exception_trace1,
                        b.business_code,
                        b.service_number,
                        i.party_role_id,
                        'N',
                        '',
                        i.create_time,
                        b.exception_time,
                        b.processinstanceid,
                        b.retry_times,
                        row_number() over(partition by b.order_id order by b.exception_time desc) exception_num
          from besorder.om_exception@to_bescust4 b
         where i.order_id = b.order_id
           and i.be_id = b.be_id;
    elsif i.indexx >= 80 and i.indexx <= 99 then
      insert into besdev.tmp_corp_failed
        select distinct b.order_id,
                        i.status,
                        b.exception_desc,
                        b.exception_trace1,
                        b.business_code,
                        b.service_number,
                        i.party_role_id,
                        'N',
                        '',
                        i.create_time,
                        b.exception_time,
                        b.processinstanceid,
                        b.retry_times,
                        row_number() over(partition by b.order_id order by b.exception_time desc) exception_num
          from besorder.om_exception@to_bescust5 b
         where i.order_id = b.order_id
           and i.be_id = b.be_id;
    end if;
  end loop;

  update besdev.tmp_corp_failed a
     set a.is_CRA = 'Y'
   where a.exception_trace1 like '%CRA%';
  commit;

  delete from besdev.tmp_syncinfo_latest;
  commit;

  insert into besdev.tmp_syncinfo_latest t
    SELECT status_time as, a.create_order_id, a.result_code
      FROM besorder.om_corp_cra_syncinfo_cz a
     where a.create_order_id in
           (select d.create_order_id
              from (SELECT max(a.status_time) as status_time,
                           a.create_order_id
                      FROM besorder.om_corp_cra_syncinfo_cz a
                     WHERE a.create_order_id in
                           (select t1.order_id
                              from besdev.tmp_corp_failed t1
                             where t1.is_CRA = 'Y')
                     group by a.create_order_id) d)
       and a.status_time in
           (select c.status_time
              from (SELECT max(a.status_time) as status_time,
                           a.create_order_id
                      FROM besorder.om_corp_cra_syncinfo_cz a
                     WHERE a.create_order_id in
                           (select t1.order_id
                              from besdev.tmp_corp_failed t1
                             where t1.is_CRA = 'Y')
                     group by a.create_order_id) c);
  commit;
  --select count(*),create_order_id From besdev.tmp_syncinfo_latest t group by create_order_id having count(*)>1
  --select count(*),create_order_id From besdev.tmp_syncinfo_his_latest t group by create_order_id having count(*)>1

  merge into (select t1.*
                from besdev.tmp_corp_failed t1
               where t1.is_CRA = 'Y') e --desti table
  using besdev.tmp_syncinfo_latest t2 --source table
  on (e.order_id = t2.create_order_id) --mutual column
  when matched then
    update set e.remark = t2.result_code;

  --if null get latest Records of his table
  delete from besdev.tmp_syncinfo_his_latest;
  commit;

  insert into besdev.tmp_syncinfo_his_latest t
    SELECT y.status_time, y.create_order_id, z.result_code
      FROM besorder.om_corp_cra_syncinfo_his_cz z
     inner join (SELECT max(a.status_time) as status_time, a.create_order_id
                   FROM besorder.om_corp_cra_syncinfo_his_cz a
                  WHERE a.create_order_id in
                        (select t1.order_id
                           from besdev.tmp_corp_failed t1
                          where (t1.is_CRA = 'Y' and t1.remark = 'null')
                             or (t1.is_CRA = 'Y' and t1.remark is null))
                  group by a.create_order_id) y
        on z.create_order_id = y.create_order_id
       and z.status_time = y.status_time;
  commit;
  -- if null it should check his 
  merge into (select t1.*
                from besdev.tmp_corp_failed t1
               where (t1.is_CRA = 'Y' and t1.remark = 'null')
                  or (t1.is_CRA = 'Y' and t1.remark is null)) e --desti table
  using besdev.tmp_syncinfo_his_latest t2 --source table
  on (e.order_id = t2.create_order_id) --mutual column
  when matched then
    update set e.remark = t2.result_code;

  merge into (select t1.*
                from besdev.tmp_corp_failed t1
               where t1.is_CRA = 'Y') e --desti table
  using besdev.CRA_Errors t2 --source table
  on (e.remark = t2.CRM_code) --mutual column
  when matched then
    update set e.Is_cra = t2.CRA_code;

  update besdev.tmp_corp_failed t1
     set remark = is_cra
   where t1.is_cra != 'N';
  update besdev.tmp_corp_failed t1 set is_cra = 'Y' where t1.is_cra != 'N';
  commit;

  --insert CreateCorCustomer & Batch Sale Orders
  insert into besdev.tmp_corp_failed
    select i.order_id,
           i.status,
           '',
           '',
           i.business_code,
           '',
           i.party_role_id,
           'N',
           '',
           i.create_time,
           '',
           '',
           '',
           ''
      from besorder.om_order_unclosed i
     where i.bizspecid in
           ('CustomerOrderSpec_Corp', 'GrpResSalesOrderSpec')
       and i.create_time > sysdate - days_ago;
  commit;
end prc_b2b_faild_orders;
