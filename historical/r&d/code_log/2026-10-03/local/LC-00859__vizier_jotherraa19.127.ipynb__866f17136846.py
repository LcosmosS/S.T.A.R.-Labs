# we get the conesearch  service associated to the first table
conesearch_interface = voresource.get_interface(service_type='conesearch', 
                                                keyword='J/other/RAA/19.127/table1',
                                                lax=True)
# if you get a TypeError about an unexpected keyword, check that you installed pyvo>=1.6
conesearch_service = conesearch_interface.to_service()