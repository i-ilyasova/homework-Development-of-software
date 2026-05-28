function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

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

async function loadUserData() {
  try {
    console.log('Загрузка списка пользователей...');
    const users = await fetchData('https://api.example.com/users');

    console.log('Список пользователей:');
    users.forEach((u) => console.log(`  [${u.id}] ${u.name} — ${u.email}`));

    console.log('\nПауза 1 секунда перед следующим запросом...');
    await delay(1000);

    console.log('Загрузка данных первого пользователя...');
    const user = await fetchData(`https://api.example.com/users/${users[0].id}`);

    console.log('\nДанные первого пользователя:');
    console.log(`  Имя:     ${user.name}`);
    console.log(`  Email:   ${user.email}`);
    console.log(`  Возраст: ${user.age}`);
    console.log(`  Роль:    ${user.role}`);
  } catch (error) {
    console.error('Ошибка:', error.message);
  }
}

loadUserData();
