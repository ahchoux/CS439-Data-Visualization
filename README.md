# CS439-Data-Visualization

<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<br />
<div align="center">
  <a href="https://github.com/ahchoux/CS439-Data-Visualization">
    <img src="images/bike_logo.jpg" alt="Logo" width="140">
  </a>

  <h3 align="center">Chapel Hill Bike Safety Visualization</h3>

  <p align="center">
    Interactive visualizations exploring bicycle crash data (2007–2018) in Chapel Hill, NC.
  </p>
</div>

---

## Table of Contents
1. [About The Project](#about-the-project)
   - [Built With](#built-with)
2. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
3. [Usage](#usage)
4. [Roadmap](#roadmap)
5. [Contributing](#contributing)
6. [License](#license)
7. [Contact](#contact)
8. [Acknowledgments](#acknowledgments)

---

## About The Project

<!-- [![Product Screenshot][product-screenshot]](https://example.com) --> add img of product later

### Overview  
Bike safety is a major concern in many urban areas where cars and bicycles share the road. Our project visualizes **bicycle crash data from 2007–2018 in Chapel Hill, North Carolina**, with the goal of understanding how environmental, demographic, and behavioral factors contribute to crash severity and frequency.

We designed two **interactive visualizations** to help users explore this data intuitively and identify risk patterns:

1. **Geospatial Heatmap**  
   A heatmap showing crash frequencies across Chapel Hill. Users can filter by features such as lighting condition, alcohol use, and time of day to examine when and where accidents occur most often.

2. **Grouped Histogram**  
   A histogram displaying the distribution of crash injury severity. Users can filter or group by demographic variables (e.g., age, sex) or behavioral/environmental conditions (e.g., alcohol use, direction of travel) to uncover deeper patterns.

Together, these visualizations aim to **inform cyclists, policymakers, and the public** about high-risk conditions and encourage safer commuting practices.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

### Built With

* [![Python][Python-badge]][Python-url]
* [![Matplotlib][Matplotlib-badge]][Matplotlib-url]
* [![PyQt6][PyQt6-badge]][PyQt6-url]
* [![Pandas][Pandas-badge]][Pandas-url]
* [![GeoPandas][GeoPandas-badge]][GeoPandas-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Getting Started

To get a local copy up and running, follow these steps.

### Prerequisites

Make sure you have **Python 3.9+** installed.

Install dependencies:
```bash
pip install -r requirements.txt
```

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ahchoux/CS439-Data-Visualization.git
   ```
2. Navigate into the project directory (PLACEHOLDER DIR NAME)
   ```
   cd bike-safety-viz
   ```
3. Run the visualization app (PLACEHOLDER FILENAME)
   ```
   python main.py
   ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

* Launch the app to explore crash data interactively.
* Use dropdown menus and sliders to filter by attributes such as lighting condition, alcohol involvement, or age group.
* Hover over map points or bars for detailed crash information.

### Example use cases

* Identify intersections with the highest accident density.
* Examine how time of day and alcohol use affect injury severity.
* Compare crash frequency by age or gender groups.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Roadmap

- [ ] Load and preprocess Chapel Hill crash dataset
- [ ] Implement geospatial heatmap visualization
- [ ] Implement grouped histogram visualization
- [ ] Add tooltip interactivity
- [ ] Integrate filtering by environmental and demographic factors

See the [open issues](https://github.com/ahchoux/CS439-Data-Visualization/issues) for more details or future enhancements.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contributing

We welcome feedback and contributions!
1. Fork the Project
2. Create your Feature Branch (git checkout -b feature/YourFeature)
3. Commit your Changes (git commit -m 'Add new feature')
4. Push to the Branch (git push origin feature/YourFeature)
5. Open a Pull Request

### Top Contributors:
<a href="https://github.com/ahchoux/CS439-Data-Visualization/graphs/contributors">
<img src="https://contrib.rocks/image?repo=ahchoux/CS439-Data-Visualization" alt="contrib.rocks image" />
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

Distributed under the MIT License. See LICENSE.txt for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact

Team Members:
John, Naomi, Dave, Nathan, Husain

Project Link: [https://github.com/ahchoux/CS439-Data-Visualization](https://github.com/ahchoux/CS439-Data-Visualization)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Acknowledgments

- [x] Chapel Hill Open Data Portal (Crash Data 2007–2018)
- [x] Purdue University – CS441: Data Visualization
- [x] Best README Template
- [x] Matplotlib and GeoPandas for visualization support

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->

[contributors-shield]: https://img.shields.io/github/contributors/ahchoux/CS439-Data-Visualization.svg?style=for-the-badge
[contributors-url]: https://github.com/ahchoux/CS439-Data-Visualization/graphs/contributors

[forks-shield]: https://img.shields.io/github/forks/ahchoux/CS439-Data-Visualization.svg?style=for-the-badge
[forks-url]: https://github.com/ahchoux/CS439-Data-Visualization/network/members

[stars-shield]: https://img.shields.io/github/stars/ahchoux/CS439-Data-Visualization.svg?style=for-the-badge
[stars-url]: https://github.com/ahchoux/CS439-Data-Visualization/stargazers

[issues-shield]: https://img.shields.io/github/issues/ahchoux/CS439-Data-Visualization.svg?style=for-the-badge
[issues-url]: https://github.com/ahchoux/CS439-Data-Visualization/issues

[license-shield]: https://img.shields.io/github/license/ahchoux/CS439-Data-Visualization.svg?style=for-the-badge
[license-url]: https://github.com/ahchoux/CS439-Data-Visualization/blob/main/LICENSE.txt

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/naomiyunanchen

[product-screenshot]: images/screenshot.png

[Python-badge]: https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/

[Matplotlib-badge]: https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge&logo=matplotlib&logoColor=white
[Matplotlib-url]: https://matplotlib.org/

[PyQt6-badge]: https://img.shields.io/badge/PyQt6-41CD52?style=for-the-badge&logo=qt&logoColor=white
[PyQt6-url]: https://pypi.org/project/PyQt6/

[Pandas-badge]: https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white
[Pandas-url]: https://pandas.pydata.org/

[GeoPandas-badge]: https://img.shields.io/badge/GeoPandas-43A047?style=for-the-badge&logo=python&logoColor=white
[GeoPandas-url]: https://geopandas.org/

