const sqlite3 = require('sqlite3').verbose();
const fs = require('fs');
const path = require('path');

class DatabaseManager {
  constructor(dbPath) {
    this.dbPath = dbPath;
    this.db = null;
  }

  async initialize() {
    return new Promise((resolve, reject) => {
      this.db = new sqlite3.Database(this.dbPath, (err) => {
        if (err) {
          reject(err);
          return;
        }
        
        this.createTables()
          .then(() => this.insertSeedData())
          .then(() => resolve())
          .catch(reject);
      });
    });
  }

  async createTables() {
    const schema = fs.readFileSync(path.join(__dirname, 'schema.sql'), 'utf8');
    
    return new Promise((resolve, reject) => {
      this.db.exec(schema, (err) => {
        if (err) {
          reject(err);
        } else {
          resolve();
        }
      });
    });
  }

  async insertSeedData() {
    const seedData = fs.readFileSync(path.join(__dirname, 'seed-data.sql'), 'utf8');
    
    return new Promise((resolve, reject) => {
      this.db.exec(seedData, (err) => {
        if (err) {
          // Ignore constraint errors (data might already exist)
          console.log('Seed data insertion note:', err.message);
        }
        resolve();
      });
    });
  }

  query(sql, params = []) {
    return new Promise((resolve, reject) => {
      this.db.all(sql, params, (err, rows) => {
        if (err) {
          reject(err);
        } else {
          resolve(rows);
        }
      });
    });
  }

  run(sql, params = []) {
    return new Promise((resolve, reject) => {
      this.db.run(sql, params, function(err) {
        if (err) {
          reject(err);
        } else {
          resolve({ id: this.lastID, changes: this.changes });
        }
      });
    });
  }

  async getCommand(name) {
    const commands = await this.query(
      'SELECT * FROM davinci_commands WHERE command_name = ?',
      [name]
    );
    return commands[0];
  }

  async searchCommands(query) {
    return await this.query(
      `SELECT * FROM davinci_commands 
       WHERE command_name LIKE ? OR description LIKE ? OR category LIKE ?
       ORDER BY command_name`,
      [`%${query}%`, `%${query}%`, `%${query}%`]
    );
  }

  async getCommandsByCategory(category) {
    return await this.query(
      'SELECT * FROM davinci_commands WHERE category = ? ORDER BY command_name',
      [category]
    );
  }

  async saveChatMessage(userMessage, aiResponse, generatedCode = null) {
    return await this.run(
      `INSERT INTO chat_history (user_message, ai_response, generated_code, executed)
       VALUES (?, ?, ?, ?)`,
      [userMessage, aiResponse, generatedCode, false]
    );
  }

  async updateChatExecution(chatId, executed, result = null) {
    return await this.run(
      `UPDATE chat_history 
       SET executed = ?, execution_result = ?
       WHERE id = ?`,
      [executed, result, chatId]
    );
  }

  async getChatHistory(limit = 50) {
    return await this.query(
      'SELECT * FROM chat_history ORDER BY created_at DESC LIMIT ?',
      [limit]
    );
  }

  async getUserSettings() {
    return await this.query('SELECT * FROM user_settings');
  }

  async updateUserSetting(key, value) {
    return await this.run(
      `INSERT OR REPLACE INTO user_settings (setting_key, setting_value, updated_at)
       VALUES (?, ?, DATETIME('now'))`,
      [key, value]
    );
  }

  close() {
    if (this.db) {
      this.db.close();
    }
  }
}

module.exports = DatabaseManager; 