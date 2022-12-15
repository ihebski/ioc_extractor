[![Open Source Love svg3](https://badges.frapsoft.com/os/v3/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)

# IOC Extractor

<p align="center">
  <img src="https://static1.cbrimages.com/wordpress/wp-content/uploads/2020/05/anime-eye-abilities-featured-image.jpg" heigh="150px"/>
</p>

**IOC extractor is a mini web application to parse CTI PDF reports and extract possible IOC's per page. This will reduce the work and effort realized by CTI analysts to go through long documents.**


- [x] Project in progress

## Motivation/Goals
- Personal learning journey of CTI work
- Assist CTI analysts by providing a shortcuts
- Mapping IOC's with MITRE ATT&CK

> The project is not completed and there is a room for enhancment and code improvement 

Future Notes:
- Add a parser for Docx files
- Fix issues with serialization on sqlalchemy
- Multi-threads
- Email results when finished
- Add Mitre Map
- Match extracted IOC's with threats
- Add dashboard
- UI enhancement

### Usage

* Script only
```
# Usage 

python3 ioc_extractor.py scan <PATH_PDF_REPORT>
````

* Web application
```
python3 webapp.py
````
