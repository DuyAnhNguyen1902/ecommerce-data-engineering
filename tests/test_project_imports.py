def test_project_imports():
    import config.settings
    import ingestion.database
    import ingestion.excel_reader
    import ingestion.load_raw
    import warehouse.load_warehouse
    import mart.load_mart
    import quality.data_quality

    assert True