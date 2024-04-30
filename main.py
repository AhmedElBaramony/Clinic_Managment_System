from GUI import *

# Open GUI Window (Login Page)

loginPage.show_page()
root.mainloop()

# Close Database Connection

conn.close()
cursor.close()
