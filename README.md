# maps_gaussian_area
project for making smart areas holding geo points

The idea behind this little project is that when we want to enclose a cloud of geo points,
a simple convex polygon might not be sufficient to best capture the unique geometry on itof the colud.

The main concep is to generate a topographic-like map of the surrounding area of the cloud of points 
by adding a 2d gaussian for each point and centered on it, then normalize the topoggraphic-like map 
so it changes between 0 and 1.

The second step is to choose a 'height' threshold and find the appropriate contour line or lines circling 
aroud the cloud. 

The final enclosurement might either be convex or concave - depending on the unique cloud arrangement.

![image](https://user-images.githubusercontent.com/54249683/159373575-3e89675b-a34a-4dc5-ba91-61c3dacf5c6b.png)
![image](https://user-images.githubusercontent.com/54249683/159373586-40d8520e-7e05-4e93-9498-9348d52cc0eb.png)
![image](https://user-images.githubusercontent.com/54249683/159373590-ad2b2edc-078d-4a93-b83b-2892795a9877.png)
![image](https://user-images.githubusercontent.com/54249683/159373599-ca1d807f-5bd2-4dd0-86a5-b203d9cae071.png)


