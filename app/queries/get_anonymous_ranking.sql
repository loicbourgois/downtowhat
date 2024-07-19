with q0 as (
    select *
    from anonymous_response
    where user_id = :user_id
),
q1 as (
    select 
        *,
        a as winner,
        b as loser
    from q0
    where choice = 'a'
    union all 
    select 
        *,
        b as winner,
        a as loser
    from q0
    where choice = 'b'
),
q2 as (
    select 
        option.*,
        user_id,
        1.0 as win,
        0.0 as lose
    from option
    left outer join q1
    on q1.winner = option.option_id
    where user_id is not null
),
q3 as (
    select 
        option.*,
        user_id,
        0.0 as win,
        1.0 as lose
    from option
    left outer join q1
    on q1.loser = option.option_id
    where user_id is not null
),
q3_2 as (
    select
        option.*,
        user_id,
        0.0 as win,
        0.0 as lose
    from option
    left outer join q1
    on q1.loser = option.option_id
),
q4 as (
    select * from q2
    union all select * from q3
    union all select * from q3_2
), 
q5 as (
    select 
        priority,
        option_id,
        option_label,
        sum(win) as wins,
        sum(lose) as loses,
        sum(win) + sum(lose) as total,
        sum(win) / NULLIF( sum(win) + sum(lose) , 0) as win_ratio
    from q4
    group by option_id, option_label, priority
)
select * from q5
where win_ratio is not null
order by 
    win_ratio desc,
    priority asc