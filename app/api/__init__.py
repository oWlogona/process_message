def setup_api(main_app):
    from api.route import process_api

    main_app.mount("/api/process/v1", process_api)
