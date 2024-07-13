create table option (
    option_id uuid not null,
    option_label text not null
);


create table dtw_user (
    user_id uuid not null,
    username text not null,
    password text not null
);


create type response_choice AS ENUM ('a', 'b', 'skip');


create table response (
    user_id uuid not null,
    option_a_id uuid not null,
    option_b_id uuid not null,
    choice response_choice not null
);
