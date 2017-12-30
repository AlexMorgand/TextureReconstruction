# TextureReconstruction application

You will find here a texture reconstruction application including a camera calibration process, a texture reconstruction (from a planar surface at the moment) and a visualization process using an OpenShadingLanguage (OSL) shader.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

## How to use

Please build the documentation with

```
make doc
```

to see a detailed tutorial of the application's usage.
Examples can be found in the *data* folder.

## Built With

This application requires:

* [Python](https://www.python.org/) **(2.7+)** - The web framework used
* PyQt **(4)** - Dependency Management
* [OpenCV](https://opencv.org/) **(2.4+)** - Used to generate RSS Feeds
* [OSL](https://github.com/imageworks/OpenShadingLanguage) - OpenShadingLanguage library. See the link for the other requirements.

### Installation and execution

Make sure that you have a working version of the OSL library and that the binaries **oslc** and **testshade** are correctly added to your *PATH*. Make sure that the libraries of OSL are also added to the *LD_LIBRARY_PATH*
To build the application, just run:

```
make
```

To run the application, do:

```
make run
```

## Possible extensions

* Dense reconstruction
* Pose estimation
* Texture on a mesh

## Authors

* **Alexandre Morgand** - *Initial work* - [AlexMorgand](https://github.com/AlexMorgand)


