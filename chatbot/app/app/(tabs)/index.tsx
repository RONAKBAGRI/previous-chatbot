import React, { useState, useRef } from 'react';
import { 
  View, Text, TextInput, FlatList, StyleSheet, TouchableOpacity, Image, ScrollView 
} from 'react-native';
import axios from 'axios';

const App = () => {
  const [messages, setMessages] = useState<{ id: string; text: string; isUser: boolean }[]>([]);
  const [inputText, setInputText] = useState('');
  const flatListRef = useRef<FlatList>(null);

  const sendMessage = async () => {
    if (inputText.trim()) {
      const userMessage = { id: String(messages.length + 1), text: inputText, isUser: true };
      setMessages((prevMessages) => [...prevMessages, userMessage]);

      try {
        const response = await axios.post('http://10.0.2.2:5000/chat', { message: inputText });  // For Android Emulator

        const botMessage = { id: String(messages.length + 2), text: response.data.response, isUser: false };
        setMessages((prevMessages) => [...prevMessages, botMessage]);

        // Auto-scroll to the latest message
        setTimeout(() => {
          flatListRef.current?.scrollToEnd({ animated: true });
        }, 100);
      } catch (error) {
        if (axios.isAxiosError(error)) {
          console.error("Error sending message:", error.response || error);
          if (axios.isAxiosError(error) && error.response) {
            console.error('Response data:', (error as any).response.data);
          }
        } else {
          console.error("Error sending message:", error);
        }
        if (axios.isAxiosError(error) && error.response) {
          // The server responded with a status code outside the range of 2xx
          console.error('Response data:', error.response.data);
        }
      }

      setInputText('');
    }
  };

  const startNewChat = () => {
    setMessages([]);
  };

  return (
    <View style={styles.container}>
      <Image source={require('../assets/logo.jpeg')} style={styles.logo} />
      <Text style={styles.greeting}>Hi, I'm Svaran. How can I help you today?</Text>

      {/* New Chat Button */}
      <TouchableOpacity style={styles.newChatButton} onPress={startNewChat}>
        <Text style={styles.newChatText}>+ New Chat</Text>
      </TouchableOpacity>

      <FlatList
        ref={flatListRef}
        data={messages}
        renderItem={({ item }) => (
          <View style={[styles.messageContainer, item.isUser ? styles.userMessage : styles.botMessage]}>
            <Text style={styles.messageText}>{item.text}</Text>
          </View>
        )}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.chatContainer}
        onContentSizeChange={() => flatListRef.current?.scrollToEnd({ animated: true })}
      />

      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          value={inputText}
          onChangeText={setInputText}
          placeholder="Type a message..."
          placeholderTextColor="#999"
          onSubmitEditing={sendMessage}
        />
        <TouchableOpacity onPress={sendMessage}>
          <Image source={require('../assets/send.png')} style={styles.sendIcon} />
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    padding: 16,
  },
  logo: {
    width: 100,
    height: 100,
    borderRadius: 50,
    alignSelf: 'center',
    marginBottom: 10,
  },
  greeting: {
    fontSize: 18,
    fontWeight: 'bold',
    textAlign: 'center',
    color: '#333',
    marginBottom: 10,
  },
  newChatButton: {
    backgroundColor: '#007bff',
    paddingVertical: 10,
    paddingHorizontal: 15,
    borderRadius: 10,
    alignSelf: 'center',
    marginBottom: 10,
  },
  newChatText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  chatContainer: {
    flexGrow: 1,
    justifyContent: 'flex-end',
    paddingBottom: 20,
  },
  messageContainer: {
    maxWidth: '80%',
    padding: 12,
    borderRadius: 12,
    marginVertical: 6,
  },
  userMessage: {
    backgroundColor: '#007bff',
    alignSelf: 'flex-end',
  },
  botMessage: {
    backgroundColor: '#35cc5d',
    alignSelf: 'flex-start',
  },
  messageText: {
    color: '#fff',
    fontSize: 16,
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    borderTopWidth: 1,
    borderTopColor: '#ddd',
    paddingTop: 10,
    backgroundColor: '#fff',
    paddingHorizontal: 10,
  },
  input: {
    flex: 1,
    backgroundColor: '#fff',
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 10,
    marginRight: 10,
    borderWidth: 1,
    borderColor: '#ddd',
    color: '#333',
  },
  sendIcon: {
    width: 40,
    height: 40,
    resizeMode: 'contain',
  },
});

export default App;
