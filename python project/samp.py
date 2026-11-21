import ursina

# Create the game
app = ursina.Ursina()

# Create a 3D cube
cube = ursina.Entity(
    model="cube",
    color=ursina.color.red,
    scale=2
)

# Start the game
app.run()