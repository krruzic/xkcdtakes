CREATE TABLE comics (
 comic_id integer PRIMARY KEY,
 comic_number text NOT NULL,
 title text NOT NULL,
 review_text text NOT NULL,
 sub_text text,
 rating text NOT NULL,
 link text NOT NULL
);