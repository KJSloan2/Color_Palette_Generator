# Color Palette Generator
 
This project generates a customizable color palette from a collection of input images. 
The user uploads an image collection and the color palette generator samples colors from the collection and ranks colors by their level of dominance (frequency of occurrence) acres the image collection. 
The color data is fed into a browser hosted user interface where the user can customize and download their unique color palette.

You can view a quick walkthrough of this tool in action on my Vimeo page here: [Color Palette Generator Walkthrough - Vimeo](https://vimeo.com/manage/videos/950372917)

![image](https://github.com/KJSloan2/Color_Palette_Generator/blob/main/00_resources/documentation/images/CPG_vimeoScreenShot.png)

## Components

The color palette generator interface is broken into three main components, the image space model, color space model and the palette generator. Each of these components allows the user to visualize and interact with different aspects of the color palette generating process.

![image](https://github.com/KJSloan2/Color_Palette_Generator/blob/main/00_resources/documentation/images/24072700_CPG_componentsOverview.png)

### Image Space

The image space model visualizes all the images fed into the model by the user that are used to generate the custom color palette. 
Images are represented in a 3D image similarity model space, where the closer images are to each other, the more similar their color attributes are. 
The model uses color moment indexing to calculate the similarity of each image by taking the mean, standard deviation, skew and kurtosis of the color distribution in the image. 
If you'd like to read more about these processes, please check out the blog posts on my website pertaining to this topic linked below.
\
### Blog Post Links
[Image Database Visualization - DigitalShades.net](https://www.digitalshades.work/project-blog/image-database-visualization)
\
[Image Feature Extraction - Color Moment Indexing - DigitalShades.net](https://www.digitalshades.work/project-blog/cbri)\
\
Prior to feeding images into the model, the user should sort their image collection into distinct categories. 
In this example, images are sorted into categories based on the location where they were taken and the subject matter in the image. 
Note: I have other tools in progress to help automate this process that use YOLO and VGG16 neural networks to sort images by subject mater and ad EXIF extractor to sort images based on the location where they were taken.  
By sorting images into distinct groups, the user can filter images based on location and subject mater by using the filter buttons on the right side of the window. 
For example, if you wanted to generate a palette with images form a particular location or of a particular subject mater, you can use the filter tools to filter the colors extracted from the corpus to those found in the filtered image categories.
![image](https://github.com/KJSloan2/Color_Palette_Generator/blob/main/00_resources/documentation/images/24072701_CPG_imageSpaceComponents.png)


### Color Space

The color space model visualizes palettized colors extracted from the image corpus in 3D color space. 
During the color extraction process, extracted colors are also palettized to reduce the number of unique colors to a manageable amount. 
Palettization is done using K-Means clustering and the resulting cluster centroid retains information about the cluster such as how many unique colors ended up  being grouped with the cluster and summary stats about the distribution of the cluster.  
In the 3D color space model, objects are representations  of the palletized colors, where the X, Y and Z coordinates of the object are derived from the Red, Blue and Green value of the color respectively.  
The size of the object is a representation of how many unique colors ended up in the cluster.


### Palette Generator
![image](https://github.com/KJSloan2/Color_Palette_Generator/blob/main/00_resources/documentation/images/24072701_CPG_paletteGeneratorComponents.png)
\
**Filter Sliders**
\
The user can filters colors based on their dominance level in the palette. 
The dominance level is derived from the cluster size of the color group from the K-Means clustering process and indicates how frequently the color (and similar colors) appeared across the corpus of images. 
The user can set a minimum and maximum dominance threshold and the generator will filter colors to those within the given range and update the charts in real time. 
\
\
**Download Button**
\
Below the sliders is the download button. 
After the user has made their color selections, they can click this button to download the selected colors as a CSV.
\
\
**Bar Chart**
\
The horizontal bar chart orders colors within the dominance range by level of dominance. 
The more frequently a color occurs across the corpus of images, the longer the bar and higher in the bar stack it will be. 
The user can select colors directly from the bar chart by clicking on them. 
\
\
**Dot Chart**
\
The dot chart  orders colors within the dominance range by hue value and groups colors based on generalized color groups like reds, oranges, yellows,  greens etc. 
The user can click and drag dots to move colors side by side for comparison and add the color to their custom palette by clicking on them. 
D3 event listeners respond to mouseover and click events and graphically change the bar and dot appearance upon selection. 
