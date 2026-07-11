#pragma once

#include <string>
#include <functional>
#include <map>
#include <vector>

namespace Velosia::Engine {

    // A lightweight Event Bus leveraging function callbacks.
    // In Python, this will receive callable objects (e.g. def on_player_died(): ...)
    class EventBus {
    public:
        using EventCallback = std::function<void(const std::string&)>;

        static EventBus& GetInstance() {
            static EventBus instance;
            return instance;
        }

        // Subscribe a callback function to an event type string
        void Subscribe(const std::string& eventType, EventCallback callback) {
            subscribers[eventType].push_back(callback);
        }

        // Emit an event, calling all subscribed callbacks
        void Emit(const std::string& eventType, const std::string& payload = "") {
            if (subscribers.find(eventType) != subscribers.end()) {
                for (auto& callback : subscribers[eventType]) {
                    callback(payload);
                }
            }
        }

        // Clear all subscriptions (useful for scene changes)
        void Clear() {
            subscribers.clear();
        }

    private:
        EventBus() = default;
        std::map<std::string, std::vector<EventCallback>> subscribers;
    };

}
