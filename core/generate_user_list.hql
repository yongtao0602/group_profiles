set mapred.job.queue.name = data;

insert overwrite table temp.dim_group_portrait_user partition (p_type = 'intersect', p_user = '${USER}')
select
    distinct a.user_id
from
    temp.dim_group_portrait_user as a
join
    temp.dim_group_portrait_user as b
on
    a.user_id = b.user_id and
    a.p_type = 'profile' and
    b.p_type = 'dims'
;

