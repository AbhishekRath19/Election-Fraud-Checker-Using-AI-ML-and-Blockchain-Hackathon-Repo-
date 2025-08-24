// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Voting {
    // Structure to store vote information
    struct Vote {
        uint256 userId;
        uint256 partyId;
        uint256 timestamp;
        bytes32 voteHash;
    }
    
    // Mapping to store votes by their hash
    mapping(bytes32 => Vote) public votes;
    
    // Mapping to track if a user has voted
    mapping(uint256 => bool) public userHasVoted;
    
    // Mapping to track vote counts for each party
    mapping(uint256 => uint256) public partyVoteCounts;
    
    // Event emitted when a vote is recorded
    event VoteRecorded(
        bytes32 indexed voteHash,
        uint256 userId,
        uint256 partyId,
        uint256 timestamp
    );
    
    // Event emitted when vote counts are updated
    event VoteCountUpdated(
        uint256 partyId,
        uint256 newCount
    );
    
    /**
     * @dev Record a vote on the blockchain
     * @param voteHash Hash of the vote data
     * @param userId ID of the user casting the vote
     * @param partyId ID of the party being voted for
     */
    function recordVote(
        bytes32 voteHash,
        uint256 userId,
        uint256 partyId
    ) public {
        // Check that user hasn't already voted
        require(!userHasVoted[userId], "User has already voted");
        
        // Check that the vote hash hasn't been used before
        require(votes[voteHash].timestamp == 0, "Vote already recorded");
        
        // Record the vote
        votes[voteHash] = Vote({
            userId: userId,
            partyId: partyId,
            timestamp: block.timestamp,
            voteHash: voteHash
        });
        
        // Mark user as having voted
        userHasVoted[userId] = true;
        
        // Update party vote count
        partyVoteCounts[partyId]++;
        
        // Emit events
        emit VoteRecorded(voteHash, userId, partyId, block.timestamp);
        emit VoteCountUpdated(partyId, partyVoteCounts[partyId]);
    }
    
    /**
     * @dev Check if a user has already voted
     * @param userId ID of the user to check
     * @return Boolean indicating if user has voted
     */
    function hasVoted(uint256 userId) public view returns (bool) {
        return userHasVoted[userId];
    }
    
    /**
     * @dev Get vote information by hash
     * @param voteHash Hash of the vote to retrieve
     * @return Vote structure
     */
    function getVote(bytes32 voteHash) public view returns (Vote memory) {
        return votes[voteHash];
    }
    
    /**
     * @dev Get vote count for a party
     * @param partyId ID of the party
     * @return Number of votes for the party
     */
    function getPartyVoteCount(uint256 partyId) public view returns (uint256) {
        return partyVoteCounts[partyId];
    }
}