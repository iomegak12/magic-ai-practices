# MCP - Model Context Protocol

## Overview

**Model Context Protocol (MCP)** is a standard mechanism for enriching the context of prompts (such as Resources, Samples, Tools and Prompts) so LLMs would assist Agents to use appropriate tools/resources. Building Agentic AI Systems become easier, simpler, and faster.

MCP is inspired by using **LSP (Language Server Protocol)**.

## Core Concept

- It's like a **Universal Plug and Play (USB Specification)**
- A standard protocol which allows AI models and agents to securely interact with external data sources, databases, and tools
- It simply resolves **M*N integration challenges**

## Key Features

### Open and Standards-Based
- **Open Source / Open Standard / Community Driven**
- **Language / Platform / Framework agnostic**
- **HTTPS / JSON RPC** - standards based communication protocol and messaging (JSON RPC 2.0 specification for messages)
- **Open Security Protocols / Standards support** for Authentication / Authorization (OpenID, OAuth 2.0 and JWT Token based Authentication Support)

### Service Discovery and Description
- Services are described in a standard format, which can then be discovered by Agents and LLMs
- **Service Description and Discovery Support**

### Communication Features
- Supports **One-Way, Two-Way, Events and Error Messaging**
- **Response and Streaming Features**
- **(SSE [Server-Sent Events] and Web-Sockets)**

### Developer and Industry Support
- MCP team has already built **SDKs for Major / commonly used Languages** (So you don't have to develop SDKs specific to your platform / language / Framework)
- **MCP Inspector** - Developer friend Tool for Testing MCP Servers
- **Industry / Community Acceptance and Adoption**

## Architecture and Components

### Architecture Type
- **Client-Server based Architecture**
- **Server** (A lightweight program that exposes Prompts, Resources and Tools and uses standard HTTPs / SSE / Web Sockets)
- **Client** (A component within the application that maintains a dedicated connection to the server to fetch the context)

### MCP Server Primitives

An MCP server may provide the following primitives:

1. **Prompts**
2. **Resources** (Data Files, Log Entries, Sample Records, Database Schemas)
3. **Tools**

## Use Cases

MCP enables:
- Secure interaction between AI models/agents and external systems
- Standardized access to data sources
- Simplified integration of tools and resources
- Consistent authentication and authorization
- Streamlined development of agentic AI systems

## Technical Stack

- **Protocol**: HTTPS, JSON RPC 2.0
- **Communication**: SSE (Server-Sent Events), Web Sockets
- **Security**: OpenID, OAuth 2.0, JWT Token-based Authentication
- **SDKs**: Available for major programming languages

## Benefits

1. **Standardization**: Reduces complexity of integrating multiple systems
2. **Scalability**: From M*N to M+N integration patterns
3. **Flexibility**: Platform and language agnostic
4. **Security**: Built-in support for modern authentication standards
5. **Developer-Friendly**: Pre-built SDKs and testing tools
6. **Community-Driven**: Open source with growing adoption
