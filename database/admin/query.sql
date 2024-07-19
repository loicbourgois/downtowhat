with q0 as (               
    select * from anonymous_dtw_user
),
q1 as (
    select * from option
),
q2 as (
    select * 
    from q0
    cross join q1
),
q3 as (
    select 
        *,
        a as winner,
        b as loser
    from anonymous_response
    where choice = 'a'
    union all 
    select 
        *,
        b as winner,
        a as loser
    from anonymous_response
    where choice = 'b'
),
q4 as (
    select 
        option.*,
        user_id,
        1.0 as win,
        0.0 as lose
    from option
    left outer join q3
    on q3.winner = option.option_id
    where user_id is not null
),
q5 as (
    select 
        option.*,
        user_id,
        0.0 as win,
        1.0 as lose
    from option
    left outer join q3
    on q3.loser = option.option_id
    where user_id is not null
),
q6 as (
    select * from q4
    union all select * from q5
),
q7 as (
    select 
        user_id,
        option_id,
        option_label,
        sum(win) as wins,
        sum(lose) as loses,
        sum(win) + sum(lose) as total,
        sum(win) / NULLIF( sum(win) + sum(lose) , 0) as win_ratio
    from q6
    group by user_id, option_id, option_label
),
q8 as (
    select 
        a.user_id as ua,
        b.user_id as ub,
        1.0 - abs(a.win_ratio - b.win_ratio) as score,
        a.option_id,
        a.option_label
    from q7 as a
    inner join q7 as b
    on a.option_id = b.option_id
    where a.user_id != b.user_id
),
q9 as (
    select count(*) as total_options 
    from option
),
q10 as (
    select 
        sum(score) as score_sum,
        cast(count(*) as float) as score_count,
        ua,
        ub
    from q8
    group by ua, ub
),
q11 as (
    select 
        ua,
        ub,
        score_sum / total_options as score,
        score_count / total_options as score_max,
        score_count
    from q10
    cross join q9
),
q12 as (
    select 
        *
    from q11
    order by score desc
)
select 
    q12.*,
    a.username as a,
    b.username as b
from q12
inner join anonymous_dtw_user as a
on q12.ua = a.user_id
inner join anonymous_dtw_user as b
on q12.ub = b.user_id
order by score desc
