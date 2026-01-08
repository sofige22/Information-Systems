import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector

# 1. Database Connection (Using mysql.connector as per your slides)
# Note: mysql.connector uses 'password' (not 'passwd')
con = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='root123456',
    database='FLYTAU'
)

# 2. Your specific SQL Query
query = """
SELECT 
    AVG(
        (IFNULL(Occupied.SeatsSold, 0) / PlaneCapacity.TotalSeats) * 100
    ) AS Average_Occupancy_Percentage
FROM 
    Flights F
JOIN (
    SELECT PlaneID, SUM(NumRows * NumCols) AS TotalSeats
    FROM Class
    GROUP BY PlaneID
) AS PlaneCapacity ON F.PlaneID = PlaneCapacity.PlaneID
LEFT JOIN (
    SELECT O.FlightID, COUNT(*) AS SeatsSold
    FROM Orders O
    JOIN Seats S ON O.OrderID = S.OrderID
    WHERE O.OrderStatus IN ('Completed') 
    GROUP BY O.FlightID
) AS Occupied ON F.FlightID = Occupied.FlightID
WHERE 
    F.FlightStatus = 'Landed';
"""

try:
    # 3. Execution and Data Loading
    # pandas.read_sql_query works with the connection object
    df = pd.read_sql_query(query, con)

    # We add a label for the X-axis since the query returns only one value
    df['Metric'] = 'Total Average'

    # 4. Visualization (Vertical Bar Chart)
    # Using 'bar' for a vertical column
    ax = df.plot(kind='bar', x='Metric', y='Average_Occupancy_Percentage',
                 legend=False, color='skyblue', figsize=(6, 8))

    # 5. Styling and Labels (All in English)
    plt.ylim(0, 100)  # Percentage scale
    plt.title('FLYTAU Operational Efficiency KPI', fontsize=14, pad=20)
    plt.ylabel('Occupancy Percentage (%)', fontsize=12)
    plt.xlabel('')
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    # Adding the data label on top of the bar
    for i, v in enumerate(df['Average_Occupancy_Percentage']):
        ax.text(i, v + 2, f"{round(v, 2)}%", color='navy', fontweight='bold', ha='center')

    plt.tight_layout()
    plt.show()

finally:
    # 6. Closing the connection
    con.close()