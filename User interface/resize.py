from PIL import Image

image = Image.open('output/')
image.show()
new_image = image.resize((400, 400))
new_image.save('output/image_400.jpg')

print(image.size)
print(new_image.size)
image.show()
