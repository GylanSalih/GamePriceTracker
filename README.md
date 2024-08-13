<a id="readme-top"></a>

<div align="center">

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

</div>

<!-- Badges Shields -->
[contributors-shield]: https://custom-icon-badges.demolab.com/github/contributors/GylanSalih/OrganizeMyFiles?color=FF0000&logo=group&label=Contributors&logoColor=white&style=for-the-badge&labelColor=000000
[forks-shield]: https://custom-icon-badges.demolab.com/github/forks/GylanSalih/OrganizeMyFiles?color=FF0000&logo=repo-forked&label=Forks&logoColor=white&style=for-the-badge&labelColor=000000
[stars-shield]: https://custom-icon-badges.demolab.com/github/stars/GylanSalih/OrganizeMyFiles?color=FF0000&label=Stars&style=for-the-badge&logo=star&logoColor=white&labelColor=000000
[issues-shield]: https://custom-icon-badges.demolab.com/github/issues/GylanSalih/OrganizeMyFiles?color=FF0000&logo=issue-opened&label=Issues&logoColor=white&labelColor=000000&style=for-the-badge&
[license-shield]: https://custom-icon-badges.demolab.com/github/license/GylanSalih/OrganizeMyFiles?color=FF0000&logo=law&label=License&logoColor=white&style=for-the-badge&labelColor=000000

<!-- Badges Links -->
[contributors-url]: https://github.com/GylanSalih/OrganizeMyFiles/graphs/contributors
[forks-url]: https://github.com/GylanSalih/OrganizeMyFiles/network/members
[stars-url]: https://github.com/GylanSalih/OrganizeMyFiles/stargazers
[issues-url]: https://github.com/GylanSalih/OrganizeMyFiles/issues
[license-url]: https://github.com/GylanSalih/OrganizeMyFiles/blob/main/LICENSE

# Gaming-Ebay-Scrapper

The Gaming Scraper is a Python-based tool designed to search for gaming products on eBay and analyze their prices over time. This scraper retrieves data based on user-defined search queries, applies filters, and provides insights into price trends. It also supports saving the scraped data to both CSV files and an SQLite database, allowing for long-term analysis and tracking.

## Features

- **Search eBay**: Perform searches for gaming products on eBay with customizable search queries.
- **Filter Results**: Exclude items based on user-defined keywords and languages.
- **Condition Filtering**: Filter products based on their condition (e.g., New, Like New, etc.).
- **Data Storage**: Save results to CSV files and an SQLite database for easy access and future analysis.
- **Price Trend Analysis**: Visualize historical price trends of gaming products.
- **URL Shortening**: Shorten eBay item URLs for cleaner output.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/GylanSalih/Gaming-Ebay-Scrapper
   ```

2. **Navigate to the project directory**:

   ```bash
   cd OrganizeMyFiles
   ```

3. **Install dependencies** (if any):
   The script requires Python 3.x. No additional Python packages are required.

## Usage

1. Open the script in your preferred text editor.

2. Modify the `download_folder` variable to point to the directory you want to organize:

   ```python
   download_folder = 'C:/Users/YourUsername/Downloads'
   ```

3. Run the script:

   ```bash
   python Gaming-Ebay-Scrapper.py
   ```

4. The script will organize files into subfolders within the specified directory based on their file types.

## Customization

You can customize the file types and categories by editing the `file_types` dictionary in the script:

```python
file_types = {
    'Images': ['.jpg', '.jpeg', '.png', ...],
    'Documents': ['.pdf', '.docx', ...],
    ...
}
```

Add or remove extensions as needed to fit your specific requirements.

## Logging

The script creates a `OrganizeMyFiles.log` file in the project directory, where it logs all actions such as successful file moves, error messages, and deleted empty folders.

## Contributing

If you'd like to contribute to this project, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
