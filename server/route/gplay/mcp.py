from datetime import datetime

from fastmcp import FastMCP
from google_play_scraper import search, app

from .data.app_details import AppDetails

mcp = FastMCP('gplay')

@mcp.tool()
def search_apps(keyword: str) -> str:
    """
    Search apps by keyword from Google Play Store

    Args:
        keyword (str): search keyword

    Returns:
        Comma(,) separated string of package names that are most relevant,
        ordered by relevance score in descending order (highest relevance first)
    """
    result = search(keyword, n_hits=1)
    package_names = [details['appId'] for details in result]
    return ','.join(package_names)

@mcp.tool()
def get_app_details(package_name: str):
    """
    Get app details from Google Play Store.

        App details contains following fields:

            app_id: package name
            title: app title
            summary: short description of app
            installs: app install counts
            score: average app rating score
            reviews: app review counts
            version: app version
            updated: app updated date

    Args:
        package_name (str): Unique identifier for an app

    Returns:
        json string of app details
    """
    result = app(package_name)
    updated = datetime.fromtimestamp(result['updated'])
    app_details = AppDetails(
        app_id=result['appId'],
        title=result['title'],
        summary=result['summary'],
        installs=result['realInstalls'],
        score=result['score'],
        ratings=result['ratings'],
        reviews=result['reviews'],
        version=result['version'],
        updated=updated.isoformat(),
    )
    return app_details.to_json()