useEffect(() => { listTodos().then(setTodos).catch(() => setTodos([])); }, []);
