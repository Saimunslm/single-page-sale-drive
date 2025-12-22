import os
folder = 'static/uploads'
for f in os.listdir(folder):
    size = os.path.getsize(os.path.join(folder, f))
    print(f"{f} - {size/1024:.2f} KB")
