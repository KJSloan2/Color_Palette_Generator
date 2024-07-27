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
[Image Database Visualization - DigitalShades.net](https://www.digitalshades.work/project-blog/image-database-visualization)
\
[Image Feature Extraction - Color Moment Indexing - DigitalShades.net](https://www.digitalshades.work/project-blog/cbri)\
\


Prior to feeding images into the model, the user should sort their image collection into distinct categories. 
In this example, images are sorted into categories based on the location where they were taken and the subject matter in the image. 
Note: I have other tools in progress to help automate this process that use YOLO and VGG16 neural networks to sort images by subject mater and ad EXIF extractor to sort images based on the location where they were taken.  
By sorting images into distinct groups, the user can filter images based on location and subject mater by using the filter buttons on the right side of the window. 
For example, if you wanted to generate a palette with images form a particular location or of a particular subject mater, you can use the filter tools to filter the colors extracted from the corpus to those found in the filtered image categories.

