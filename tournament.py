#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM matches")
    c.execute("alter sequence players_id_seq restart with 1")
    c.execute("alter sequence matches_id_seq restart with 1")
    c.execute("alter sequence standings_id_seq restart with 1")
    DB.commit()
    DB.close()

def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM players")
    c.execute("DELETE FROM standings")
    DB.commit()
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT count(*) FROM players")
    results = c.fetchone()
    DB.close()
    return results[0]

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    name = bleach.clean(name)
    DB = connect()
    c = DB.cursor()

    """ Add playser to players table"""
    c.execute("INSERT INTO players (name) VALUES (%s)",
      (name,))

    """ Add playser to standings table"""
    c.execute("INSERT INTO standings (name, wins, matches) VALUES (%s,%s,%s)",
      (name,0,0))
    DB.commit()
    DB.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    c = DB.cursor()
    """ Select and order all the players in the standings table """
    c.execute("SELECT * FROM standings order by wins ASC")
    DB.commit()
    results = c.fetchall()
    DB.close()
    return results

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    
    """ Add a match to the matches table """
    c.execute("INSERT INTO matches (winner, loser) VALUES (%s, %s)",
      (winner,loser,))
    
    """ Update the standings table with winners"""
    c.execute("UPDATE standings SET wins = wins + 1, matches = matches + 1 where id = (%s)",(winner,))
    
    """ Update the standings table with matches"""
    c.execute("UPDATE standings SET matches = matches + 1 where id = (%s)",(loser,))
    DB.commit()
    DB.close()
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    DB = connect()
    c = DB.cursor()
    """ Get standings """
    standings = playerStandings()
    data = standings
    """ pair standings by every 2 """
    pairings = []
    for i,k in zip(data[0::2], data[1::2]):
        
        pairings.append([i[0], i[1], k[0], k[1]])    
    return pairings
    DB.close()

