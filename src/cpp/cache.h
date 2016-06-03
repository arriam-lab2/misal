#pragma once

#include <unordered_map>
#include <list>
#include <string>
#include <iterator>
#include <mutex>

#include <iostream>

namespace concurrent
{
    template <class Key,
              class T,
              class Compare = std::less<Key>>
    class lru_cache
    {
    public:
        // Member types
        typedef Key key_type;
        typedef T mapped_type;
        typedef std::pair<const Key, T> value_type;
        typedef size_t size_type;

        // TODO; typedef difference_type //

        typedef Compare key_compare;

    private:
        typedef std::list<value_type> cache_list;
        typedef typename cache_list::iterator list_entry;
        typedef std::unordered_map<Key, list_entry> cache_map;

    public:
        typedef typename cache_list::iterator iterator;
        typedef typename cache_list::const_iterator const_iterator;

    public:
        // ctors
        explicit lru_cache(size_t max_size = 50, const Compare& comp = Compare())
            : _max_size(max_size)
        {}

        lru_cache(const lru_cache&) = delete;
        lru_cache(lru_cache&&) = delete;
        lru_cache& operator=(const lru_cache&) = delete;
        lru_cache& operator=(lru_cache&&) = delete;

        ~lru_cache()
        {}

        // TODO: element access

        T& operator[](const Key& key)
        {
            std::lock_guard<std::mutex> lock(_mutex);
            iterator it = _map[key];
            it = _splay(it);
            assert(it == _last());
            return it->second;
        }

        // TODO: iterators

        // Capacity

        bool empty()
        {
            return _list.empty();
        }

        size_t size()
        {
            return _list.size();
        }

        size_t max_size()
        {
            return _max_size;
        }

        // Modifiers
        void clear()
        {
            std::lock_guard<std::mutex> lock(_mutex);
            _list.clear();
            _map.clear();
        }

        std::pair<iterator, bool> insert(const value_type& pair)
        {
            std::lock_guard<std::mutex> lock(_mutex);
            auto found = _map.find(pair.first);
            if (found != _map.end())
            {
                return std::make_pair(_last(), false);
            }
            else
            {
                return _lru_insert(pair);
            }
        }

        // TODO: Lookup

        // TODO: Observers

    private:
        std::pair<iterator, bool> _lru_insert(const value_type& pair)
        {
            if (_list.size() == _max_size)
            {
                _lru_delete();
            }
            return _insert_back(pair);
        }

        void _lru_delete()
        {
            assert(!empty());

            iterator elem = _list.begin();
            key_type key = elem->first;
            _list.erase(elem);
            _map.erase(key);
        }

        std::pair<iterator, bool> _insert_back(const value_type& pair)
        {
            _list.push_back(pair);
            iterator last = _last();
            _map[pair.first] = last;
            return std::make_pair(last, true);
        }

        iterator _last()
        {
            assert(!empty());

            iterator last = _list.end();
            std::advance(last, -1);
            return last;
        }

        iterator _splay(iterator pos)
        {
            auto pair = _insert_back(*pos);
            _list.erase(pos);
            return pair.first;
        }

    private:
        cache_list _list;
        cache_map _map;
        size_t _max_size;
        std::mutex _mutex;
    };


}