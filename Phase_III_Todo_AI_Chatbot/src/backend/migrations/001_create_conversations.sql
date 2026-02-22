-- Migration: 001_create_conversations.sql
-- Purpose: Create conversations and messages tables for Phase-III AI Chatbot
-- Date: 2026-02-17
-- Author: Phase-III Implementation

-- ============================================================================
-- Create conversations table
-- ============================================================================

CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add indexes for performance
CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_conversations_updated_at ON conversations(updated_at DESC);

-- Add comment
COMMENT ON TABLE conversations IS 'Chat conversations between users and AI assistant';
COMMENT ON COLUMN conversations.id IS 'Unique identifier for the conversation';
COMMENT ON COLUMN conversations.user_id IS 'Foreign key to user table - ensures user isolation';
COMMENT ON COLUMN conversations.created_at IS 'When the conversation was started';
COMMENT ON COLUMN conversations.updated_at IS 'Last activity timestamp (auto-updated via trigger)';

-- ============================================================================
-- Create messages table
-- ============================================================================

CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add indexes for performance
CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_messages_conv_created ON messages(conversation_id, created_at DESC);

-- Add comments
COMMENT ON TABLE messages IS 'Individual messages within conversations';
COMMENT ON COLUMN messages.id IS 'Unique identifier for the message';
COMMENT ON COLUMN messages.conversation_id IS 'Foreign key to conversations table';
COMMENT ON COLUMN messages.role IS 'Message sender: user or assistant';
COMMENT ON COLUMN messages.content IS 'The actual message text';
COMMENT ON COLUMN messages.created_at IS 'When the message was sent';

-- ============================================================================
-- Create trigger for auto-updating conversation.updated_at
-- ============================================================================

-- Create or replace the trigger function
CREATE OR REPLACE FUNCTION update_conversation_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Drop trigger if exists (for re-running migration)
DROP TRIGGER IF EXISTS trg_update_conversation_timestamp ON conversations;

-- Create the trigger
CREATE TRIGGER trg_update_conversation_timestamp
    BEFORE UPDATE ON conversations
    FOR EACH ROW
    EXECUTE FUNCTION update_conversation_updated_at();

-- ============================================================================
-- Verification queries
-- ============================================================================

-- Verify tables were created
-- SELECT 
--     table_name,
--     'Created: ' || COALESCE(obj_description(oid, 'pg_class'), 'No comment') as description
-- FROM information_schema.tables
-- WHERE table_schema = 'public'
--   AND table_name IN ('conversations', 'messages');

-- Verify indexes
-- SELECT 
--     tablename,
--     indexname,
--     indexdef
-- FROM pg_indexes
-- WHERE schemaname = 'public'
--   AND tablename IN ('conversations', 'messages')
-- ORDER BY tablename, indexname;

-- Verify trigger
-- SELECT 
--     trigger_name,
--     event_manipulation,
--     event_object_table,
--     action_statement
-- FROM information_schema.triggers
-- WHERE trigger_schema = 'public'
--   AND event_object_table = 'conversations';

-- ============================================================================
-- Rollback (for undoing this migration)
-- ============================================================================

-- To rollback, run:
-- DROP TRIGGER IF EXISTS trg_update_conversation_timestamp ON conversations;
-- DROP FUNCTION IF EXISTS update_conversation_updated_at();
-- DROP TABLE IF EXISTS messages;
-- DROP TABLE IF EXISTS conversations;

-- ============================================================================
-- Sample data (for testing - optional)
-- ============================================================================

-- Uncomment to insert test data:
-- INSERT INTO conversations (id, user_id, created_at, updated_at)
-- VALUES 
--     ('00000000-0000-0000-0000-000000000001', 'test-user-id', NOW(), NOW());

-- INSERT INTO messages (conversation_id, role, content, created_at)
-- VALUES 
--     ('00000000-0000-0000-0000-000000000001', 'user', 'Hello!', NOW()),
--     ('00000000-0000-0000-0000-000000000001', 'assistant', 'Hi! How can I help you?', NOW());
