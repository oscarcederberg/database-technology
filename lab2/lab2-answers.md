# Lab 2 Answers

## Which relations have natural keys?
Theatres has the unique names of the theatres, costumers have usernames, tickets have IDs, and movies have IMDB-Keys.

## Is there a risk that any of the natural keys will ever change?
In a real-world situation, theatres can rebrand/rename and usernames might also be changeable. Tickets most likely won't change IDs, and IMDB-keys are probably not changing either.

## Are there any weak entity sets?
Yes. Performance is a weak entity as it can only be uniquely identified by a compund with foreign keys (theatre, movie, and starttime).

## In which relations do you want to use an invented key. Why?
Pefromances could use an invented key instead of a compound one, it makes it easier to describe tickets if they have one. Ticket IDs are defined in the problem very similar to the functionality of invented keys.

## There are at least two ways of keeping track of the number of seats available for each performance – describe them both, with their upsides and downsides
1. Group tickets by performance, count the number of tickets for each performance and compare to the capacity of the theatre. + No extra attributes to keep track of. - Have to query each time it needs to be checked.
2. Keep track of number of free seats (or taken seats) for each performance. + No need to query each time, just check the value. - Extra bookkeeping.