/* SQL Exercise
====================================================================
We will be working with database chinook.db
You can download it here: https://drive.google.com/file/d/0Bz9_0VdXvv9bWUtqM0NBYzhKZ3c/view?usp=sharing&resourcekey=0-7zGUhDz0APEfX58SA8UKog

 The Chinook Database is about an imaginary video and music store. Each track is stored using one of the digital formats and has a genre. The store has also some playlists, where a single track can be part of several playlists. Orders are recorded for customers, but are called invoices. Every customer is assigned a support employee, and Employees report to other employees.
*/

-- MAKE YOURSELF FAIMLIAR WITH THE DATABASE AND TABLES HERE





--==================================================================
/* TASK I
Which artists did not make any albums at all? Include their names in your answer.
A: 71 entries
*/

SELECT artists.Name 
    FROM artists
    LEFT OUTER JOIN albums
    ON artists.ArtistId = albums.ArtistId
    WHERE albums.AlbumId IS NULL
    ORDER BY artists.Name ASC;



/* TASK II
Which artists recorded any tracks of the Latin genre?
A: 28 artists
*/

SELECT artists.Name
    FROM artists
    JOIN albums
    ON artists.ArtistId = albums.ArtistId
    JOIN tracks
    ON albums.AlbumId = tracks.AlbumId
    JOIN genres
    ON tracks.GenreId = genres.GenreId
    WHERE tracks.GenreId IN (SELECT GenreId FROM genres 
                            WHERE genres.Name = 'Latin')
    GROUP BY artists.Name;

/* TASK III
Which video track has the longest length?
3	Protected MPEG-4 video file
A: Occupation / Precipice, 5286953 Milliseconds
*/

SELECT tracks.Name, MAX(Milliseconds)
    FROM tracks
    JOIN media_types
    ON tracks.MediaTypeId = media_types.MediaTypeId
    WHERE media_types.MediaTypeId = 3;

/* TASK IV
Find the names of customers who live in the same city as the top 
employee (The one not managed by anyone - EmployeeId = 1).
A: Mark	Philips
*/

SELECT customers.FirstName, customers.LastName 
    FROM customers
    WHERE customers.City = (SELECT employees.City 
                        FROM employees WHERE EmployeeId = 1);

/* TASK V
Find the managers of employees supporting Brazilian customers.
A: Nancy Edwards
*/

SELECT 
    e.FirstName,
    e.LastName,
    e.EmployeeId
FROM
    employees e
LEFT JOIN     
    (SELECT DISTINCT
        e.EmployeeId,
        e.ReportsTo
    FROM 
        employees e
    JOIN 
        customers c
    ON 
        e.EmployeeId = c.SupportRepId
    WHERE 
        c.Country = 'Brazil') r
WHERE 
    e.EmployeeId = r.ReportsTo
GROUP BY e.EmployeeId;


/* TASK VI
Which playlists have no Latin tracks?
A: 11 playlists
*/
WITH
playlist_name AS (
SELECT 
    p.Name,
    pt.TrackId
FROM 
    playlists p
JOIN
    playlist_track pt
ON p.PlaylistId = pt.PlaylistId
),

genre_name AS (
SELECT 
    g.Name,
    t.TrackId
FROM 
    genres g
JOIN
    tracks t
ON g.GenreId = t.GenreId
)


SELECT
    p.Name
FROM
    playlist_name p
LEFT JOIN
    genre_name g
ON
    p.TrackId = g.TrackId
WHERE
    g.Name != 'Latin'
GROUP BY
    p.Name;