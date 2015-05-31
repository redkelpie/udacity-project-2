-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Create the tournament database
CREATE DATABASE tournament;

-- Create the players table where player names and ID will be stored
CREATE TABLE players (id SERIAL PRIMARY KEY,
                     name VARCHAR(128) NOT NULL);

-- Create the players table where matches
CREATE TABLE matches (id SERIAL PRIMARY KEY,
                     winner INT NOT NULL references players(id),
                     loser INT NOT NULL references players(id));

-- Create the players table where standings
CREATE TABLE standings (id SERIAL PRIMARY KEY,
					name VARCHAR(128), 
					wins INT DEFAULT 0, 
					matches INT DEFAULT 0);
CREATE TABLE swiss_pairings (id SERIAL PRIMARY KEY,
					round INT DEFAULT 0,
					player_name VARCHAR(128), 
					player_id INT NOT NULL references players(id));
