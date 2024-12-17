# Dell-Lookup Scripts

*Useful scripts that work nicely with this client.*

---

### `bulk-model-add.py`
Adds model number and warranty start date to a CSV.

Expects schema:
```
Service Tag,PKID,Express Service Code,Serial Number
```

Which is standard Dell order report format.

Serial number is usually blank for each. Script references `Service Tag`

Takes CSVs from the current working directory. If > 100 service tags, additional logic may be required to work with Dell API limtations.