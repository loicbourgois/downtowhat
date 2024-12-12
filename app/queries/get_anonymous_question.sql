with q0 as (
    select *
    from anonymous_response
    where user_id = :user_id
),
q1 as (
    select 
        a as c1,
        b as c2
    from q0
    union all 
    select 
        b as c1,
        a as c2
    from q0
),
q3 as (
    select a as response_id from q0
    union all
    select b as response_id from q0
),
q4 as (
    select 
        response_id,
        count(*) as count_
    from q3
    group by response_id
),
q5 as (
    select *
    from option
    left outer join q4
    on option.option_id = response_id
),
q6 as (
    select 
        option_id as a,
        option_label as a_label,
        count_,
        priority,
        grouping as a_grouping
    from q5
),
q7 as (
    select 
        q6.priority,
        count_,
        a_grouping,
        q6.a,
        q6.a_label,
        cosine_similarity,
        b,
        t2.grouping as b_grouping,
        t2.option_label as b_label
    from q6
    inner join cosine_similarity as t1
    on t1.a = q6.a
    inner join option as t2
    on t2.option_id = t1.b
),
q8 as (
    select
        count_,
        priority,
        a_grouping,
        a,
        a_label,
        cosine_similarity,
        b,
        b_grouping,
        b_label,
        CASE WHEN b_grouping = a_grouping
            THEN 1
            ELSE 2
        END AS grouping_match  
    from q7
    left outer join q1
    on q7.a = q1.c1 and q7.b = q1.c2
    where c1 is null
    order by 
        count_ asc NULLS FIRST,
        priority asc,
        grouping_match asc,
        cosine_similarity desc
)
select * from q8
limit 1
