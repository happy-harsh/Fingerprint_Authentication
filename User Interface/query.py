import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyBDexR0M6wBSeAyfCUJhAkzC9Mi2zjmCNk",
    "authDomain": "firepro-b51c3.firebaseapp.com",
    "databaseURL": "https://firepro-b51c3-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "firepro-b51c3",
    "storageBucket": "firepro-b51c3.appspot.com",
    "messagingSenderId": "316408109669",
    "appId": "1:316408109669:web:103b3b60826b6acc43848c",
    "measurementId": "G-3XZ7JTSPYN"
}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()

# Delete item with known key
db.child("todolistA").child("wednesday").child(
    "volunteer").child("deadline").remove()

# Delete entire node and its children
db.child("todolistA").child("tuesday").remove()

# Delete item with unkown generated key
monday_tasks = db.child("todolistB").child("monday").get()

for task in monday_tasks.each():
    if task.val()['name'] == "paper":
        key = task.key()

db.child("todolistB").child("monday").child(key).child("deadline").remove()
