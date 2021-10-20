
import cv2
import pandas as pd

img_path = 'pic2.jpg'
csv_path = 'colors.csv'

# reading csv file
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
df = pd.read_csv(csv_path, names=index, header=None)

# reading image
img = cv2.imread(img_path)
img = cv2.resize(img, (800, 600))

# declaring global variables
clicked = False
r = g = b = xpos = ypos = 0

# function to calculate minimum distance from all colors and get the most matching color
def get_color_name(r, g, b):
	minimum = 1000
	for i in range(len(df)):
		d = abs(r - int(df.loc[i,'R'])) + abs(g - int(df.loc[i,'G'])) + abs(b - int(df.loc[i,'B']))
		if d <= minimum:
			minimum = d
			cname = df.loc[i, 'color_name']

	return cname

#function to get x,y coordinates of mouse double click
def draw_function(event, x, y, flags, params):
	if event == cv2.EVENT_LBUTTONDBLCLK:
		global B, G, R, xpos, ypos, clicked
		clicked = True
		xpos = x
		ypos = y
		B,G,R = img[y,x]
		B = int(B)
		G = int(G)
		R = int(R)

# creating window
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while True:
	cv2.imshow('image', img)
	if clicked:
		#cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle 
		cv2.rectangle(img, (20,20), (600,60), (B,G,R), -1)

		#Creating text string to display( Color name and RGB values )
		text = get_color_name(R,G,B) + ' R=' + str(R) + ' G=' + str(G) + ' B=' + str(B)
		#cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
		cv2.putText(img, text, (50,50), 2,0.8, (255,255,255),2,cv2.LINE_AA)

		#For very light colours we will display text in black colour
		if r+g+b >=600:
			cv2.putText(img, text, (50,50), 2,0.8, (0,0,0),2,cv2.LINE_AA)

	if cv2.waitKey(20) & 0xFF == 27:
		break

cv2.destroyAllWindows()
