function fetchData(url) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const db = {
        'https://api.example.com/users': [
          { id: 1, name: 'Алиса', email: 'alice@example.com' },
          { id: 2, name: 'Боб',   email: 'bob@example.com'   },
          { id: 3, name: 'Вера',  email: 'vera@example.com'  },
        ],
        'https://api.example.com/users/1': {
          id: 1, name: 'Алиса', email: 'alice@example.com', age: 28, role: 'admin',
        },
      };

      if (url in db) {
        resolve(db[url]);
      } else {
        reject(new Error(`Ресурс не найден: ${url}`));
      }
    }, 2000);
  });
}

fetchData('https://api.example.com/users')
  .then((users) => {
    console.log('Список пользователей:');
    users.forEach((u) => console.log(`  [${u.id}] ${u.name} — ${u.email}`));
    return fetchData(`https://api.example.com/users/${users[0].id}`);
  })
  .then((user) => {
    console.log('\nДанные первого пользователя:');
    console.log(`  Имя:    ${user.name}`);
    console.log(`  Email:  ${user.email}`);
    console.log(`  Возраст: ${user.age}`);
    console.log(`  Роль:   ${user.role}`);
  })
  .catch((error) => {
    console.error('Ошибка загрузки данных:', error.message);
  });
