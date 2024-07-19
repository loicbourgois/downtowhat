create type response_choice AS ENUM ('a', 'b', 'skip');


create table option (
    grouping int not null,
    priority int not null,
    option_id text not null,
    option_label text not null
);


create table cosine_similarity (
    a text not null,
    b text not null,
    cosine_similarity float not null
);


create table dtw_user (
    user_id uuid not null,
    username text not null,
    email text not null,
    password text not null
);


create table response (
    user_id uuid not null,
    a text not null,
    b text not null,
    choice response_choice not null
);


create table anonymous_dtw_user (
    user_id uuid not null,
    public_user_id uuid not null,
    username text not null
);


create table anonymous_response (
    user_id uuid not null,
    a text not null,
    b text not null,
    choice response_choice not null
);


ALTER TABLE option ADD CONSTRAINT pk_option PRIMARY KEY (option_id);
CREATE INDEX idx_option_priority ON option (priority);


ALTER TABLE cosine_similarity ADD CONSTRAINT pk_cosine_similarity PRIMARY KEY (a,b);
ALTER TABLE cosine_similarity ADD FOREIGN KEY (a) REFERENCES option(option_id);
ALTER TABLE cosine_similarity ADD FOREIGN KEY (b) REFERENCES option(option_id);


ALTER TABLE dtw_user ADD CONSTRAINT pk_dtw_user PRIMARY KEY (user_id);
ALTER TABLE dtw_user ADD CONSTRAINT unique_dtw_user_email UNIQUE (email); 


ALTER TABLE response ADD FOREIGN KEY (user_id) REFERENCES dtw_user(user_id);


ALTER TABLE anonymous_dtw_user ADD CONSTRAINT pk_anonymous_dtw_user PRIMARY KEY (user_id);


ALTER TABLE anonymous_response ADD FOREIGN KEY (user_id) REFERENCES anonymous_dtw_user(user_id);
