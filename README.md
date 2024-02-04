<div align="center" id="top"> 
  <a href="https://github.com/micaelcosmo/rpa_challenge_pixeldu">rpa_challenge_pixeldu</a>
</div>

<p></p>

<h1 align="center">RPA Challenge - PixelDu</h1>

<p align="center"> 
Welcome to the RPA Challenge - PixelDu project! This repository contains the code and resources used in the RPA challenge. 
</p>

<p align="center">
  <img alt="Github top language" src="https://img.shields.io/github/languages/top/micaelcosmo/rpa_challenge_pixeldu?color=56BEB8">
</p>

<p align="center">
  <img alt="Github language count" src="https://img.shields.io/github/languages/count/micaelcosmo/rpa_challenge_pixeldu?color=56BEB8">
</p>

<hr>

<p align="center">
  <a href="#about">About</a> &#xa0; | &#xa0; 
  <a href="#technologies">Technologies</a> &#xa0; | &#xa0;
  <a href="#requirements">Requirements</a> &#xa0; | &#xa0;
  <a href="#getting-started">Getting Started</a> &#xa0; | &#xa0;
  <a href="https://github.com/micaelcosmo" target="_blank">Author</a>
</p>

<br>

## About ##

The challenge is to automate data extraction from a news site through a Robocloud process. The parameters, received via Robocloud work items, include a search phrase, news category, and the number of months for news retrieval. The process involves navigating the news site, entering search phrases, selecting categories, and extracting title, date, description, and image filename. The data is then stored in an Excel file with additional details like search phrase count and money presence in title/description.

## Technologies ##

The following tools were used in this project:

- [Python](https://www.python.org/)
- [Selenium](https://www.selenium.dev/)
- [RPAFramework](https://rpaframework.org/)
- [Logging](https://docs.python.org/3/library/logging.html)

## Requirements ##

Before starting, you need to have [Git](https://git-scm.com) and [Conda](https://conda.io/projects/conda/en/latest/index.html) installed.

## Getting Started ##

### Download Project

You can download the project by cloning the repository:

```bash
git clone https://github.com/micaelcosmo/rpa_challenge_pixeldu.git
```

### Install Conda

Make sure you have Conda installed on your system. If not, you can download and install it from [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html).

### Create Conda Environment

Navigate to the project directory and create a Conda environment using the provided `conda.yaml` file:

```bash
cd rpa_challenge_pixeldu
conda env create -n rpa_challenge_env -f conda.yaml
```

This will create a virtual environment named `rpa_challenge_env` with all the necessary dependencies.

### Activate Conda Environment

Activate the Conda environment:

```bash
conda activate rpa_challenge_env
```

## Running the Project

Now that you have set up the environment, you can run the project using the following command:

```bash
python main.py
```

This will execute the main script and start the RPA challenge for PixelDu.

## Conclusion

You are now ready to get excel result file with news data! If you encounter any issues or have questions, feel free to check the documentation or reach out to the project maintainers.


Made by <a href="https://github.com/micaelcosmo/" target="_blank">Micael cosmo</a>

&#xa0;

<a href="#top">Back to top</a>
