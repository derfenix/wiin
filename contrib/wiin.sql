-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler  version: 0.7.0
-- PostgreSQL version: 9.3
-- Project Site: pgmodeler.com.br
-- Model Author: ---

SET check_function_bodies = false;
-- ddl-end --

-- object: wiin | type: ROLE --
-- DROP ROLE wiin;
CREATE ROLE wiin WITH 
	LOGIN
	UNENCRYPTED PASSWORD 'secret';
-- ddl-end --


-- Database creation must be done outside an multicommand file.
-- These commands were put in this file only for convenience.
-- -- object: wiin | type: DATABASE --
-- -- DROP DATABASE wiin;
-- CREATE DATABASE wiin
-- 	ENCODING = 'UTF8'
-- ;
-- -- ddl-end --
-- 

-- object: public.users | type: TABLE --
-- DROP TABLE public.users;
CREATE TABLE public.users(
	id serial NOT NULL,
	name varchar(300) NOT NULL,
	email varchar(254) NOT NULL,
	created timestamp NOT NULL,
	auth_key varchar(254) NOT NULL,
	fb_id varchar(255) NOT NULL,
	active boolean DEFAULT True,
	CONSTRAINT users_id PRIMARY KEY (id),
	CONSTRAINT users_fb_id_uniq UNIQUE (fb_id)

);
-- ddl-end --
-- object: email_idx | type: INDEX --
-- DROP INDEX public.email_idx;
CREATE INDEX email_idx ON public.users
	USING hash
	(
	  email
	);
-- ddl-end --


ALTER TABLE public.users OWNER TO wiin;
-- ddl-end --

-- object: public.brands | type: TABLE --
-- DROP TABLE public.brands;
CREATE TABLE public.brands(
	id serial NOT NULL,
	name varchar(254) NOT NULL,
	created timestamp NOT NULL,
	CONSTRAINT brands_id PRIMARY KEY (id)

);
-- ddl-end --
ALTER TABLE public.brands OWNER TO wiin;
-- ddl-end --

-- object: public.brand_follows | type: TABLE --
-- DROP TABLE public.brand_follows;
CREATE TABLE public.brand_follows(
	user_id serial NOT NULL,
	brand_id serial NOT NULL
);
-- ddl-end --
-- object: users_brands_follows_idx | type: INDEX --
-- DROP INDEX public.users_brands_follows_idx;
CREATE INDEX users_brands_follows_idx ON public.brand_follows
	USING btree
	(
	  user_id,
	  brand_id
	);
-- ddl-end --


ALTER TABLE public.brand_follows OWNER TO wiin;
-- ddl-end --

-- object: public.brand_likes | type: TABLE --
-- DROP TABLE public.brand_likes;
CREATE TABLE public.brand_likes(
	user_id serial NOT NULL,
	brand_id serial NOT NULL,
	created timestamp NOT NULL
);
-- ddl-end --
-- object: users_brands_likes_idx | type: INDEX --
-- DROP INDEX public.users_brands_likes_idx;
CREATE INDEX users_brands_likes_idx ON public.brand_likes
	USING btree
	(
	  user_id,
	  brand_id
	);
-- ddl-end --


ALTER TABLE public.brand_likes OWNER TO wiin;
-- ddl-end --

-- object: public.posts | type: TABLE --
-- DROP TABLE public.posts;
CREATE TABLE public.posts(
	id integer NOT NULL,
	brand_id serial NOT NULL,
	title varchar(500) NOT NULL,
	text text,
	url varchar(600),
	image_url varchar(350),
	created timestamp NOT NULL,
	CONSTRAINT posts_id PRIMARY KEY (id)

);
-- ddl-end --
-- object: brand_posts | type: INDEX --
-- DROP INDEX public.brand_posts;
CREATE INDEX brand_posts ON public.posts
	USING btree
	(
	  brand_id ASC NULLS LAST
	);
-- ddl-end --


ALTER TABLE public.posts OWNER TO wiin;
-- ddl-end --

-- object: public.posts_likes | type: TABLE --
-- DROP TABLE public.posts_likes;
CREATE TABLE public.posts_likes(
	post_id integer NOT NULL,
	user_id integer NOT NULL
);
-- ddl-end --
ALTER TABLE public.posts_likes OWNER TO wiin;
-- ddl-end --

-- object: public.posts_links_followed | type: TABLE --
-- DROP TABLE public.posts_links_followed;
CREATE TABLE public.posts_links_followed(
	post_id serial NOT NULL,
	user_id serial NOT NULL
);
-- ddl-end --
-- object: posts_links_useres_idx | type: INDEX --
-- DROP INDEX public.posts_links_useres_idx;
CREATE INDEX posts_links_useres_idx ON public.posts_links_followed
	USING btree
	(
	  post_id,
	  user_id
	);
-- ddl-end --


ALTER TABLE public.posts_links_followed OWNER TO wiin;
-- ddl-end --

-- object: public.posts_comments | type: TABLE --
-- DROP TABLE public.posts_comments;
CREATE TABLE public.posts_comments(
	id serial NOT NULL,
	post_id serial NOT NULL,
	user_id serial NOT NULL,
	text text NOT NULL,
	created timestamp NOT NULL,
	CONSTRAINT comment_id PRIMARY KEY (id)

);
-- ddl-end --
-- object: posts_users_comments_idx | type: INDEX --
-- DROP INDEX public.posts_users_comments_idx;
CREATE INDEX posts_users_comments_idx ON public.posts_comments
	USING btree
	(
	  post_id ASC NULLS LAST,
	  user_id
	);
-- ddl-end --


ALTER TABLE public.posts_comments OWNER TO wiin;
-- ddl-end --

-- object: user_id | type: CONSTRAINT --
-- ALTER TABLE public.brand_follows DROP CONSTRAINT user_id;
ALTER TABLE public.brand_follows ADD CONSTRAINT user_id FOREIGN KEY (user_id)
REFERENCES public.users (id) MATCH FULL
ON DELETE CASCADE ON UPDATE NO ACTION;
-- ddl-end --


-- object: brand_id | type: CONSTRAINT --
-- ALTER TABLE public.brand_follows DROP CONSTRAINT brand_id;
ALTER TABLE public.brand_follows ADD CONSTRAINT brand_id FOREIGN KEY (brand_id)
REFERENCES public.brands (id) MATCH FULL
ON DELETE CASCADE ON UPDATE NO ACTION;
-- ddl-end --


-- object: user_id | type: CONSTRAINT --
-- ALTER TABLE public.brand_likes DROP CONSTRAINT user_id;
ALTER TABLE public.brand_likes ADD CONSTRAINT user_id FOREIGN KEY (user_id)
REFERENCES public.users (id) MATCH FULL
ON DELETE CASCADE ON UPDATE NO ACTION;
-- ddl-end --


-- object: brand_id | type: CONSTRAINT --
-- ALTER TABLE public.brand_likes DROP CONSTRAINT brand_id;
ALTER TABLE public.brand_likes ADD CONSTRAINT brand_id FOREIGN KEY (brand_id)
REFERENCES public.brands (id) MATCH FULL
ON DELETE CASCADE ON UPDATE NO ACTION;
-- ddl-end --


-- object: brand_id | type: CONSTRAINT --
-- ALTER TABLE public.posts DROP CONSTRAINT brand_id;
ALTER TABLE public.posts ADD CONSTRAINT brand_id FOREIGN KEY (brand_id)
REFERENCES public.brands (id) MATCH FULL
ON DELETE CASCADE ON UPDATE NO ACTION;
-- ddl-end --


-- object: post_id | type: CONSTRAINT --
-- ALTER TABLE public.posts_likes DROP CONSTRAINT post_id;
ALTER TABLE public.posts_likes ADD CONSTRAINT post_id FOREIGN KEY (post_id)
REFERENCES public.posts (id) MATCH FULL
ON DELETE CASCADE ON UPDATE NO ACTION;
-- ddl-end --


-- object: user_id | type: CONSTRAINT --
-- ALTER TABLE public.posts_likes DROP CONSTRAINT user_id;
ALTER TABLE public.posts_likes ADD CONSTRAINT user_id FOREIGN KEY (user_id)
REFERENCES public.users (id) MATCH FULL
ON DELETE CASCADE ON UPDATE NO ACTION;
-- ddl-end --


-- object: post_id | type: CONSTRAINT --
-- ALTER TABLE public.posts_links_followed DROP CONSTRAINT post_id;
ALTER TABLE public.posts_links_followed ADD CONSTRAINT post_id FOREIGN KEY (post_id)
REFERENCES public.posts (id) MATCH FULL
ON DELETE CASCADE ON UPDATE NO ACTION;
-- ddl-end --


-- object: user_id | type: CONSTRAINT --
-- ALTER TABLE public.posts_links_followed DROP CONSTRAINT user_id;
ALTER TABLE public.posts_links_followed ADD CONSTRAINT user_id FOREIGN KEY (user_id)
REFERENCES public.users (id) MATCH FULL
ON DELETE CASCADE ON UPDATE NO ACTION;
-- ddl-end --


-- object: post_id | type: CONSTRAINT --
-- ALTER TABLE public.posts_comments DROP CONSTRAINT post_id;
ALTER TABLE public.posts_comments ADD CONSTRAINT post_id FOREIGN KEY (post_id)
REFERENCES public.posts (id) MATCH FULL
ON DELETE CASCADE ON UPDATE NO ACTION;
-- ddl-end --


-- object: user_id | type: CONSTRAINT --
-- ALTER TABLE public.posts_comments DROP CONSTRAINT user_id;
ALTER TABLE public.posts_comments ADD CONSTRAINT user_id FOREIGN KEY (user_id)
REFERENCES public.users (id) MATCH FULL
ON DELETE CASCADE ON UPDATE NO ACTION;
-- ddl-end --


-- object: grant_a4289a447d | type: PERMISSION --
GRANT CREATE,USAGE
   ON SCHEMA public
   TO wiin WITH GRANT OPTION;
-- ddl-end --

-- object: grant_043e54b245 | type: PERMISSION --
GRANT CREATE,CONNECT,TEMPORARY
   ON DATABASE wiin
   TO wiin WITH GRANT OPTION;
-- ddl-end --


