/* Welcome to the SQL mini project. For this project, you will use
Springboard' online SQL platform, which you can log into through the
following link:

https://sql.springboard.com/
Username: student
Password: learn_sql@springboard

The data you need is in the "country_club" database. This database
contains 3 tables:
    i) the "Bookings" table,
    ii) the "Facilities" table, and
    iii) the "Members" table.

Note that, if you need to, you can also download these tables locally.

In the mini project, you'll be asked a series of questions. You can
solve them using the platform, but for the final deliverable,
paste the code for each solution into this script, and upload it
to your GitHub.

Before starting with the questions, feel free to take your time,
exploring the data, and getting acquainted with the 3 tables. */



/* Q1: Some of the facilities charge a fee to members, but some do not.
Please list the names of the facilities that do. */

SELECT ccf.facid, ccf.name, ccf.membercost

FROM country_club.Facilities ccf

WHERE 1=1 
	AND ccf.membercost > 0

Tennis Court 1
Tennis Court 2
Massage Room 1
Massage Room 2
Squash Court 

/* Q2: How many facilities do not charge a fee to members? */
SELECT COUNT(DISTINCT ccf.facid)

FROM country_club.Facilities ccf

WHERE 1=1 
	AND ccf.membercost = 0

/* Q3: How can you produce a list of facilities that charge a fee to members,
where the fee is less than 20% of the facility's monthly maintenance cost?
Return the facid, facility name, member cost, and monthly maintenance of the
facilities in question. */

SELECT 
	ccf.facid
	,ccf.name
	,ccf.membercost
	,ccf.monthlymaintenance

FROM country_club.Facilities ccf

WHERE 1=1 
	-- Charge fee to members
	AND ccf.membercost > 0
	-- AND fee is < 20% of facility's monthly maintenance cost
	AND ccf.membercost < (0.2 * ccf.monthlymaintenance)


/* Q4: How can you retrieve the details of facilities with ID 1 and 5?
Write the query without using the OR operator. */
SELECT 
	ccf.*

FROM country_club.Facilities ccf 

WHERE 1=1
	AND ccf.facid in (1,5)


/* Q5: How can you produce a list of facilities, with each labelled as
'cheap' or 'expensive', depending on if their monthly maintenance cost is
more than $100? Return the name and monthly maintenance of the facilities
in question. */

SELECT 
	ccf.name 
	,ccf.monthlymaintenance
	,CASE
		WHEN ccf.monthlymaintenance > 100 THEN 'expensive'
		ELSE 'cheap' END as labelled

FROM country_club.Facilities ccf

WHERE 1=1 
	


/* Q6: You'd like to get the first and last name of the last member(s)
who signed up. Do not use the LIMIT clause for your solution. */
SELECT *
FROM (
	SELECT 
		ccm.firstname
		,ccm.surname
		,ccm.joindate
		,(@row_number:=@row_number + 1) as num

	FROM 
		country_club.Members ccm 
		,(SELECT @row_number:=0) as t

	WHERE 1=1

	ORDER BY 
		ccm.joindate desc
)a

WHERE 1=1 
	AND num = 1

/* Q7: How can you produce a list of all members who have used a tennis court?
Include in your output the name of the court, and the name of the member
formatted as a single column. Ensure no duplicate data, and order by
the member name. */
SELECT DISTINCT 
	ccf.name 
	,concat(ccm.firstname,' ',ccm.surname) as member_name

FROM country_club.Facilities ccf 
JOIN country_club.Bookings ccb ON ccf.facid = ccb.bookid
JOIN country_club.Members ccm ON ccb.memid = ccm.memid

WHERE 1=1 
	AND ccf.name in ('Tennis Court 1','Tennis Court 2')

ORDER BY concat(ccm.firstname,' ',ccm.surname)


/* Q8: How can you produce a list of bookings on the day of 2012-09-14 which
will cost the member (or guest) more than $30? Remember that guests have
different costs to members (the listed costs are per half-hour 'slot'), and
the guest user's ID is always 0. Include in your output the name of the
facility, the name of the member formatted as a single column, and the cost.
Order by descending cost, and do not use any subqueries. */

SELECT 
	ccf.name 
	,concat(ccm.firstname,' ',ccm.surname) as member_name
	,ccb.memid
	,CASE 
		WHEN ccb.memid = 0 THEN ccf.guestcost
		ELSE ccf.membercost END as fac_cost

FROM country_club.Bookings ccb
LEFT JOIN country_club.Facilities ccf ON ccb.facid = ccf.facid
LEFT JOIN country_club.Members ccm ON ccb.memid = ccm.memid

WHERE 1=1 
	AND ccb.starttime between '2012-09-14' and '2012-09-14 23:59:59'
	-- Costs
	AND (
		-- Guests
		(
			ccb.memid = 0
			AND ccf.guestcost > 30
		)
		-- Members
		OR ( 
			ccb.memid != 0
			AND ccf.membercost > 30
		)
	)

ORDER by 4 desc


/* Q9: This time, produce the same result as in Q8, but using a subquery. */
SELECT 
	*
FROM (
	SELECT 
		ccf.name 
		,concat(ccm.firstname,' ',ccm.surname) as member_name
		,ccb.memid
		,CASE 
			WHEN ccb.memid = 0 THEN ccf.guestcost
			ELSE ccf.membercost END as fac_cost

	FROM country_club.Bookings ccb
	LEFT JOIN country_club.Facilities ccf ON ccb.facid = ccf.facid
	LEFT JOIN country_club.Members ccm ON ccb.memid = ccm.memid

	WHERE 1=1 
		AND ccb.starttime between '2012-09-14' and '2012-09-14 23:59:59'
)a 

WHERE 1=1 
	AND fac_cost > 30

ORDER by 4 desc



/* Q10: Produce a list of facilities with a total revenue less than 1000.
The output of facility name and total revenue, sorted by revenue. Remember
that there's a different cost for guests and members! */


SELECT 
	a.name 
	,SUM(a.fac_cost) as total_revenue
FROM (
	SELECT 
		ccf.name 
		,concat(ccm.firstname,' ',ccm.surname) as member_name
		,ccb.memid
		,CASE 
			WHEN ccb.memid = 0 THEN ccf.guestcost
			ELSE ccf.membercost END as fac_cost

	FROM country_club.Bookings ccb
	LEFT JOIN country_club.Facilities ccf ON ccb.facid = ccf.facid
	LEFT JOIN country_club.Members ccm ON ccb.memid = ccm.memid

	WHERE 1=1 
		-- AND ccb.starttime between '2012-09-14' and '2012-09-14 23:59:59'
)a 

GROUP BY 1
HAVING SUM(a.fac_cost) < 1000

ORDER BY 2